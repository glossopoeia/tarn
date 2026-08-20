# Round 13 triage — implementer-consequence lens

## Disclosure

Read: `spec/tarn.md` only (§§2.1, 2.2, 2.3, 2.5, 4.7, 5.2, 6.1, 7.2, 7.3, 7.4,
8.1, 9.7, 10.2, 10.3, 11.1–11.4, 16.1, 16.2, 17.3, 17.4, 18.2, 20.3, 21.1–21.9,
24, Appendix G, Appendix H, front matter). No walk transcripts opened. No
`transcript-triage-*` opened.

**Protocol slip, disclosed:** my first command included `ls` of
`scratchpad/round13/`, which the brief told me not to do. The listing showed
only walk transcripts, three quiz transcripts and four `.py` files — no
`transcript-triage-*` file existed at that moment, so nothing from another
pass reached me.

Ran: one python count over the register cells (below).

## Mechanical check of §21.8's total

Script over lines 3200–3370, splitting each Instances cell on `;` and counting
`—` as 1:

    rows 121  instances 264

So §21.8's "121 conditions over 264 instances" reproduces exactly against the
cells as written. The instance-criterion findings are therefore *not* arithmetic
errors; they are about whether the criterion was applied evenly.

## Grouping

| group | ids |
|---|---|
| metadata-encoding "unassigned" over-reach | reader-01, writer-01, diagrams-03, adversary-02 |
| §21.1 instance criterion applied unevenly | reader-02, diagrams-01, register-03 |
| §24's §21.1 renumbering citation | verifier-02, diagrams-06, register-01 |
| §20.3/§11.1 "a geometry change renumbers ordinals" | diagrams-02 |
| [R-WRT-04] freeze: enumeration vs effect test | writer-02 |
| §11.1 Rationale's flat no-shrink claim | adversary-05 |
| [R-SLB-04] trigger under-covers a re-partition | writer-03 |
| Appendix G item 3 record order circular | writer-04, diagrams-04, adversary-04 |
| F33's gloss drops [R-CNT-13]'s third case | register-04, adversary-03 |
| partial slack total for a rejected layer | verifier-01 |
| front-block check in the verifier checklist | adversary-01 |
| §21.7 omits [R-CNT-18]'s nesting prohibition | register-02 |
| §4.7's stated layout-table columns | diagrams-05 |
| §21.9's "finding aid rather than an inventory" | register-05 |

24 ids in, 24 placed, none twice.

Splits I deliberately did **not** merge:

- writer-02 and adversary-05 both attack the §20.3 declaration freeze from the
  "stated more broadly than the effect warrants" direction, but the defective
  sentence is different (normative enumeration vs non-normative Rationale) and
  so is the repair. Kept apart; a reconciler merging them loses nothing.
- diagrams-02 and adversary-05 both quote §11.1's Rationale. Different clauses
  ("disk ordinals renumber" vs "extents ... do not shrink"), different math.

## Per-group verification and the downgrade quotations

### 1. metadata encoding — checked against the text, not the reporters

§10.2's table: metadata encoding assigned 1,2 / reserved 3–0x7F / experimental
≥0x80. §21.5's preamble excepts "an unassigned encoding". R1, four lines below,
registers "a document encoding of 0, or a reserved-range value (3-0x7F)".
§21.6's row is scoped "experimental-range (≥ 0x80)". So the preamble's word is
wrong; it means *experimental*. Appendix H repeats the loose word.

Does anything license verifier B to certify a file carrying encoding 0x05?

- R1's own row text names the range, with detector `reader` and detection point
  `open (top-level)`.
- [R-EXT-03]: "a value from a reserved range MUST NOT be emitted at all before
  this specification assigns it".
- [R-MTA-10] expressly preserves the check: file conformance "is decided by the
  structural checks that precede the document alone: the record's framing and
  extent slot (`[R-CNT-13]`), the encoding byte's own value set
  (`[R-MTA-03]`), and the extent's terminal CRC (`[R-CNT-20]`)".
- §21.5's own next sentence: "Every row here is a violation all the same".
- The preamble's cross-reference points at §21.6, whose only row on the subject
  says ≥ 0x80 — following the pointer refutes the reading it was offered for.
- Appendix H disclaims itself: "each entry's authority is the requirement or
  section cited, never this summary."

Same shape as the record-type space, where reserved is F36/L25 (violation) and
experimental is §21.6 (conforming). Downgrade stands: editorial.

### 2. instance criterion

Cells as written: T3 = 6, T14 = 6 (longer/shorter × 3 layouts); T21 = 3, T22 = 3
(layouts only); L21 = "—" = 1; L22 = 3 with the plain inequality as one; L44 = 3.
Structurally identical predicates, three treatments. §21.1's own escape —
"the count is therefore mechanical once the cell is written" — puts the
discretion in the cell, which makes the criterion unfalsifiable but the total
well defined. Verified 264 mechanically. Nothing here changes a detection point
or an outcome: T14's outcome is reject-tile at tile use under [R-COD-04]
whichever way its cell reads. Register-bookkeeping.

### 3. §24's citation

`grep -n "renumber\|positional\|struck"` → §2.2 (identifiers, opposite
property), §11.1 and §20.3 (disk ordinals), §24 itself. §21.1 states no
row-label policy. The pointer does not land, and the policy §24 asserts exists
nowhere else while ~15 in-document cross-references (§9.6, §17.2, §21.1's own
specialization list, F33, T2/T13/T15/T16/T23/T26, §21.6, Appendix H) rely on
row labels being citable. Editorial, with a maintenance decision attached.

### 4. "a geometry change renumbers ordinals"

[R-GEO-06]: s = Σᵢ tᵢ · ∏_{j>i} Gⱼ. The i = 0 term's product runs over j > 0,
so s is independent of G₀. Interleaved d = 2, G = (4,4) → s = 4t₀ + t₁; grow
E₀ so G = (7,4) → s = 4t₀ + t₁, unchanged. At d = 1, s = t₀ always. So the
gloss is false for growth of the first-declared axis in an interleaved layer,
and true for planar (c·N + s moves every block with c ≥ 1) and for interleaved
when a later grid count changes. §16.2's worked case in writer-03 is the
converse: growing the *last* axis does renumber.

Byte consequence: none. [R-GEO-06] is the document's only ordinal formula and
§20.3 cites it as the parenthetical's authority rather than offering a
procedure, so a writer computing entry positions has exactly one recipe and two
writers emit identical index regions. Editorial — but it is a false statement
inside normative text, not a Note.

### 5. [R-WRT-04]'s enumeration — the closest call in this batch

Witness 1 verified against [R-COD-10]: "for a packed boolean plane s = 1 and
the filter is the identity", and for an interleaved single-uint8-channel layer
s = Q = 1, so byte i of group j lands at i·n + j = j. Filter 1 ↔ 2 is a no-op
there. Witness 2 verified: E 4→3 with T 4 leaves G = 1, makes in-tile ordinal 3
a padding position, and [R-SER-05]'s fill is already the stored 0x00.
Witness 3 is in the paragraph itself: "an extent MAY always **grow**", which
alters the padding set of every stored edge tile. So the closing universal —
"Every such change makes each stored tile it reaches nonconforming" — is false
under the literal reading of the enumeration.

Why this is not byte-level. Both updaters emit a *conforming file*: the layer
declares filter 2, the stored bytes shuffle at stride 1 to the same image, no
§21 row fires, and a verifier walks the live state only (§9.7: "Nothing here
enumerates prior commits"). [R-CNF-02] decides the status of those bytes without
reference to how they were reached: "File conformance is a pure predicate on
bytes: it does not depend on any reader, writer, or environment." What forks is
one updater's *permission to reach that file by a commit*, not the set of
byte sequences that are conforming, nor any verifier verdict. I record this as
the batch's nearest miss and would not object if a reconciler re-flagged it.

### 6. §11.1's Rationale on shrinking

`grep -n shrink` → exactly one hit, line 1461, inside a Rationale. §2.1: "All
text in this document is normative except: §1 (Introduction); any text labeled
*Note*, *Example*, or *Rationale*". So nothing normative bars a shrink, and
§20.3's rule bars only what alters a stored tile's §14 facts. adversary-05's
worked case (E 5→4 with T 4, tile 0 stored and all-real) verified: G 2→1,
entry_count 2→1, tile 0's decoded size, sample offsets, padding set (empty
before and after) and codec unchanged. The Rationale over-states the rule.

### 7. [R-SLB-04]

Reproduced the witness. Interleaved, dims y(E2,T1), x(E2,T1), G = (2,2), N = 4,
S = 2, A_slab = 4096, tiles at 4096, 4097, 8192, 8193. Runs [0,2) and [2,4):
both first-tile-aligned and packed. Grow E_x to 3: G_x = 3, s = 3t₀ + t₁, so
ordinals are 0→(0,0)@4096, 1→(0,1)@4097, 2→new, 3→(1,0)@8192, 4→(1,1)@8193,
5→new. Runs [0,2), [2,4), [4,6). Run [4,6)'s first stored tile is at 8193, and
8193 mod 4096 = 1 → L42.

The commit changed no tile's storedness and no tile's offset, so [R-SLB-04]'s
trigger ("changes the stored-tile set or the byte placement of any run") is at
best arguable. But the file's status is not: [R-SLB-03] binds "When declared,
for every run: ... the first stored tile's offset satisfies offset mod
A_slab = 0", unconditionally on the file, and L42 registers the failure as
reject-layer at certification. So the updater that carries the declaration
forward emits a file every verifier reports nonconforming under either reading
of [R-SLB-04], and [R-CNF-05]/[R-CNF-06] make that updater nonconforming. No
verdict forks; the trigger still under-covers and should be widened.

### 8. Appendix G item 3

§7.2's header puts extent_offset at bytes 8–15 and extent_length at 16–23, so a
record's "encoded bytes" contain values the placement order fixes, and item 3
fixes placement by "ascending record order" — the order being defined. Two
records of one type agreeing on flags and inline_length have two self-consistent
orders. The "save that type 0x0001 ties by layer name" clause is the same
circularity already patched for layer records. [R-CNT-14] caps type 0x0002 at
one per scope and L26 bars 0x0001 from sub-record sequences, so the general
clause is reachable only for unassigned types. Downgrade quote, from the
appendix's own opening: "It adds no requirement to any actor: a writer ignoring
it is fully conforming." Both fixed points are conforming files; no reader or
verifier verdict turns on which a writer picked.

### 9. F33

[R-CNT-13] names three: "a verifier MUST treat an intra-layer overlap ... as
reject-layer, any overlap across layers or touching another scope's structures
as reject-file, and any overlap between two structures neither of which belongs
to a layer as reject-file". F33's em-dash gloss carries two. Its head clause
("two structures that do not belong to the same layer") and its Instances cell
("record extents; ... directory region") both cover the third. §21.1: "where a
row and the rule it cites diverge, **the rule governs**". Verdict fixed;
the gloss should be extended. Register-bookkeeping.

### 10. Partial slack total

§5.2's aside: "a rejected layer's claimants are not enumerated, whether or not
the rejection impeded reading them" — declarative, and the "whether or not"
clause is vacuous under the reporter's reading (b). §9.7 says the same in its
own words: "a scope-level rejection blocks enumeration". The text decides
reading (a); what is genuinely defective is that a stipulation about the walk is
buried in an em-dash aside inside an em-dash list, where its normative force is
easy to miss. PARTIAL, editorial.

### 11. Front block

§8.1's map: "Front signature block | none — checked by byte equality (§6.1)",
so §9.7's "each verifies against the checksum covering it, where §8.1's map
states one" indeed does not reach it, and Appendix H's verifier checklist —
the document's own enumeration of "the checks readers are exempt from" — omits
it. Decided against the exemption by §2.3: "**Conforming verifier.** A reader
that additionally checks every file-level requirement — including those
ordinary readers are exempted from — and certifies conformance", reinforced by
[R-CNF-11] confining *cannot establish* to "a capability or resource ground".
Real hazard, cheap repair: one clause in Appendix H's verifier list.

### 12. §21.7 and [R-CNT-18]

§21.1 designates "§21.7 the account, by class, of what fails" the detectability
gate. §21.7's second paragraph names [R-LIF-01]/[R-LIF-03], [R-GEO-06]/
[R-SER-01], [R-CNT-13]'s no-embedded-offsets clause, and [R-ENC-06]. The
nesting prohibition's account lives only in §7.4's Note ("in format major 1 it
has no reader-detectable witness, and so no register row"), on a fifth ground.
"by class" is a genuine hedge, so this is an accounting gap, not a
contradiction. Register-bookkeeping.

### 13. Layout-table columns

Headers as they stand: §6.1 `Offset|Size|Value|Class` (4); §6.2, §15.1, §18.2
`Offset|Size|Type|Field|Class|Valid values` (6); §7.2 `Offset|Size|Type|Field|
Class` (5); §7.4 `Field|Type|Constraint` (3). §4.7's Note promises six and
carves out §7.4 alone. Three of six keep the promise. The front matter already
hedges ("columns suit the structure"). Non-normative Note; every field's
offset, width, type and range remains recoverable. Editorial.

### 14. §21.9's framing

"this section collects the ones an implementer most often needs at hand, and is
a finding aid rather than an inventory — each limit is normative where the
structure forcing it is defined" scopes over the whole section, and the
minimum-guarantee table is in the section, is normative in situ under
[R-ERR-03], and no structure forces its figures (grep confirms rank 32, C 4096,
2³², 65,536, 16 MiB, 256 MiB, 8 MiB appear only in §21.9's table, its own Note,
and sections citing §21.9). Decided against the mis-reading by [R-ERR-03] in the
same paragraph — "a conforming reader MUST accept any conforming file whose
quantities lie within these bounds" — and by §2.5: "MUST accept any conforming
file within the minimum guarantees stated in §21's limits table ... the table is
§21.9". Editorial.

## Byte-level count

0. The two I re-opened before settling were the [R-WRT-04] freeze (group 5) and
the metadata-encoding preamble (group 1); the reasoning and the deciding
quotations are above.
