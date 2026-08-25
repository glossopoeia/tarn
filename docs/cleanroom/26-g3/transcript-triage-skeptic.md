# Round 26 triage — skeptic pass, working transcript

## What I read

Only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, via `sed`/`grep`.
Sections opened in full: 2.1, 2.3, 3.1, 4.2, 5.1, 5.2, 6.1, 6.2, 6.3, 7.4's
worked example and closing Note, 9.2, 9.6, 9.7, 11.1, 11.2, 11.3, 11.4, 13.3,
15.1, 15.2, 15.3, 16 preamble, 16.1, 16.2, 17.2, 17.3, 17.4, 19.1, 19.2, 19.3
opening, 19.4, 20.3, 20.4, 21.1, 21.2, 21.3, 21.4, 21.6, 21.7, 21.8,
Appendix A, Appendix G.

I read **no** transcript in round26/ — not a walk transcript, not a triage
transcript. I listed the directory once with `ls | head -1` before I had read
the prohibition carefully; the single line it printed was `calc.py`. No
`transcript-triage-*.md` name was displayed and none was opened. I did not
repeat the listing.

I evaluated all 25 findings. No finding was left unjudged.

## Method

Skeptic's default: hunt for the sentence that forecloses the finding. Where I
found one I quote it. Where I searched and could not find one, I say so.

---

## Group 1 — §11.1's bolded "last" (reader-02, writer-01, verifier-03, adversary-02, quiz-02)

Five reporters, one sentence. All five census the word, all five conclude the
positional house sense makes the sentence false, all five pick "final
remaining", all five flag not-byte-level.

Text as it stands (§11.1 Rationale):

> Growth that leaves **entry_count** unchanged touches the directory alone —
> a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0
> among them, the product holding at 0. Growth that changes entry_count
> changes extent_length with it (`[R-CNT-17]`), ... — the growth that raises
> a zero-extent layer's **last** zero grid count included.

Tried to kill it with: the preceding sentence. It genuinely does disambiguate
by contrast — the previous sentence takes "raising one grid count while
another stays 0" and the trailing clause must therefore take the complementary
case, i.e. the final remaining zero. So a reader who does the arithmetic gets
there. But that is context resolving a word against the document's own
uniform usage, not a sentence deciding it, and I could find no sentence that
defines "last" in the final-remaining sense anywhere. Confirmed the census
spot-checks myself: §11.4 "the last-declared dimension varies fastest";
§16.2's Note "a run is a band along the last-declared dimension"; §11.2's
Example "the last row of tiles is padded"; §21.9 "The last three rows";
Appendix G item 2 "the digest's **last eight bytes** in output order", which
goes out of its way to guard a positional word. Two of the positional uses
index a dimension, which is exactly what a grid count is indexed by.

CONFIRMED, editorial. Repair: "last **remaining** zero grid count", two words,
no counts move. Not byte-level: [R-CNF-01] — "All text in this document is
normative except: §1 (Introduction); any text labeled *Note*, *Example*, or
*Rationale*" — and the same Rationale defers in terms ("§20.3 states
normatively, and governs"). [R-CNT-17]/L22 and §20.3 step 4 fix the emitted
bytes under either reading.

## Group 2 — §13.3's "Note — sparse writing" states the trigger short (reader-01, writer-02, diagrams-03, quiz-03)

Note: "each commit that changes a layer's stored-tile set, or that grows its
extents so that entry_count changes, re-emits that layer's whole tile-index
region".

Rule, §20.3 step 4: "Every layer whose stored-tile set **or index content**
this commit changes has its tile-index region re-emitted in full".

Tried to kill it by loosening "stored-tile set". §3.1 forecloses that:
"A tile is *stored in a generation* if and only if that generation's
tile-index entry for it is not the sentinel". A supersede leaves every entry
non-sentinel, so the set is unchanged. §20.4 confirms the document uses the
strict sense where it matters: "Superseding a stored tile's bytes re-places
that layer's index region (§20.3, `[R-WRT-04]`), moving its extent slot (§7.4)
and so modifying that layer's record" — a sentence that would be redundant
under the loose reading. §5.1's Example carries both disjuncts. And under the
loose reading "or index content" in both §20.3 and §5.1 would be dead text.

So the Note is short by: (a) supersede, (b) a shrink that changes entry_count
(§20.3 says so in terms: "`[R-CNT-17]` obliges the smaller entry_count and so
a re-emitted index region"), and (c) reader-01's renumbering commit — extents
(2,3) → (3,2) at tile extents (1,1), entry_count fixed at 6, extent_length
fixed, stored set fixed, every ordinal moved by [R-GEO-06]. I checked (c)
against §20.3 step 4 and it is covered there — "(a geometry change renumbers
ordinals wherever `[R-GEO-06]` moves them)" — and covered by the "index
content" disjunct, which is the disjunct the Note drops. §21.7 does confirm
the wrong-ordinal outcome is unwitnessed. That is the worst of the three
failure modes and it is real.

CONFIRMED, editorial. Repair: make the Note quote the rule — "each commit that
changes a layer's stored-tile set or its index content". Not byte-level:
[R-CNF-01] puts the Note outside normative text and §20.3 step 4 governs; and
each mistaken writer's output is caught (L22) or is a conforming-but-wrong
file whose bytes were emittable anyway.

## Group 3 — §20.3's cost Note instances the trigger with a commit that does not fire it (diagrams-02)

> **Note.** ... any change to a layer's stored-tile set re-emits that layer's
> whole tile-index region, so editing one sample of a 10⁶-tile layer appends
> about 20 MB of index

Distinct sentence from group 2's, distinct repair, so a separate group.
Same §3.1 argument: editing one sample supersedes a stored tile and leaves the
stored-tile set alone, so the "so" does not follow from the trigger named.
I looked for a sentence licensing the loose sense and found the opposite in
§20.4 (quoted above). CONFIRMED, editorial: name both disjuncts, or say
"any change to a layer's index".

## Group 4 — §21.7's second paragraph (writer-03, register-04)

Both report the same defect: the paragraph enumerates unwitnessed obligations
and omits siblings. register-04's sweep is a superset of writer-03's single
item ([R-LIF-02] step 3).

Tried to kill it, and largely succeeded. §21.1:

> The subsections after §21.5 are not part of the register and carry no rows:
> neither this completeness clause nor the instance arithmetic below reaches
> §21.6's defined non-violations, **§21.7's account of what no check
> detects**, or §21.9's limits.

and

> ... detectability being the gate `[R-CNF-07]` already applies and §21.7 the
> account, **by class**, of what fails it

So the normative completeness clause expressly does not reach §21.7, and §21.7
is a class account. The class §21.7 opens with — "A second set of obligations
is omitted from the register because a single file exhibits no witness of
their violation" — does cover every member both reporters name. The gap
claim is therefore refuted.

What survives is the unevenness: the paragraph itemizes [R-WRT-06]'s four
sub-obligations while leaving [R-CNT-08]'s updater clause, [R-WRT-05],
[R-WRT-07], [R-WRT-08], [R-WRT-03], [R-WRT-09] and [R-LIF-02] step 3 unnamed —
and §9.2's own Note singles out step 3's violation. PARTIAL, editorial:
an "among them" or "for example" would make the class reading unmissable.

## Group 5 — Appendix G's closing paragraph omits the filter (writer-04)

Checked the enumeration item by item. The closing list names gap content, gap
extent, record and sub-record order, the default fill, the all-fill sentinel,
a single generation, alignment and slab, version_minor, a derived file_id, NFC
names, and the producer pinning of items 1 and 9. Item 5's second half — "**A
fixed filter value** likewise" — is not there. The reporter is right on the
facts.

Deciding sentence, which the reporter quotes and then argues past:

> Read the numbered items as the list; this paragraph names what they are for,
> not how many there are.

"Read the numbered items as the list" is a direct instruction that the
paragraph is not the authority, so an adopter auditing against the summary
alone is doing what the appendix told them not to. PARTIAL, editorial: add
"a filter value, which §17.3 leaves to the writer" to the list; nothing else
moves.

## Group 6 — Appendix G item 5's justification is false at stride 1 (writer-05)

Item 5: "it changes the stored bytes of every tile it touches".
[R-COD-10]: "for a packed boolean plane s = 1 and the filter is the identity",
and the shuffle at s = 1 maps offset j to i·n + j with i ≡ 0, i.e. to j.
So the transform is the identity for every packed planar bool plane, every
planar plane of a one-byte-element channel, and every interleaved layer with
sample stride Q = 1.

Searched for the appendix rescuing itself and found the normative text saying
the opposite instead — §20.3 step 4:

> a change that leaves every one of those tiles' stored bytes meaning exactly
> what they meant — a filter whose mandated stride makes it the identity
> (`[R-COD-10]`) ... — is not what this bars.

So the document knows the identity case normatively and denies it in the
appendix. CONFIRMED, editorial. Item 5's conclusion survives on the layer
record's filter field (01 vs 02), which is what the sentence should say. Not
byte-level: Appendix G "adds no requirement to any actor: a writer ignoring it
is fully conforming"; a misled writer declines a permitted commit rather than
emitting different bytes.

## Group 7 — Appendix G never fixes "the same input" (diagrams-04)

Item 5's three-part test — the specification leaves the choice to the writer,
the choice changes stored bytes, no content implies it — is satisfied verbatim
by layout ([R-SER-06] leaves both values open; N vs C·N changes entry_count and
the whole index region) and by tile extents (§11.3's Note: "Tile extents are a
writer's choice, and this specification imposes none"). Neither is pinned, and
the closing paragraph says "Everything else the profile needs is already
mandatory".

Searched for a definition of the profile's input and did not find one. Item 2
is the nearest thing — "two files carrying the same arrays can legitimately
differ in tiling, layout, and codec" — and it cuts both ways: it treats tiling
and layout as free given the same arrays, while the profile pins alignment,
slab and filter, which are declarations of exactly the same kind. Note also
that item 1 pins the *encoder implementation*, not the codec value, which is
evidence the drafters treat declarations as input; item 5 then pins three
declarations anyway. That inconsistency is the finding.

CONFIRMED, editorial. Repair is the maintainer's choice: state in the opening
what "the same input" fixes, or add layout and tile extents to item 5. Not
byte-level: "It adds no requirement to any actor: a writer ignoring it is
fully conforming", and [R-CNF-05] already licenses divergent conforming bytes.

## Group 8 — §20.3 step 4 and a change to C or d (writer-06)

Hunted hard here. The bar is stated over declarations generally; the worked
permissions are extents only. The clause I found that decides the reporter's
question:

> Dropping a tile out of the addressed set (§11.2's grid count falls) is not
> itself such an alteration — **a tile the new state does not address carries
> no §14 obligation and its extent becomes slack**

and, two sentences later:

> What counts as such an alteration is the bar above and nothing else, its
> carve-out included

The reason given is stated generally — "a tile the new state does not address"
— not restricted to the parenthetical's mechanism, and the closing sentence
makes the bar the whole test. So reading (A), permitted, is decided; the
reporter picked (A) and was right, but had to generalize the parenthetical to
get there. That generalization is the cost.

PARTIAL, design-decision: the maintainer should say outright whether a commit
may change C or d, since the permission currently arrives only by extending a
parenthetical written for extents. Not byte-level, and here is the premise so
someone can attack it: [R-CNF-02] makes file conformance "a pure predicate on
bytes", and the byte sequence the reporter's C=4→C=2 commit produces is
emittable by a permitted route (a fresh creation of the same live state), so
no byte sequence moves between emittable and non-emittable; §21.7 independently
records that the bar has no witness where the affected tiles leave the live
state. If someone can show a byte sequence reachable under (A) and reachable
by no permitted route under (B), this downgrade fails.

## Group 9 — [R-ENC-04]'s scope and Gᵢ·Tᵢ (verifier-01) — the one flagged byte-level

This is the finding I tried hardest to uphold, and it died on two sentences.

First, [R-GEO-03], normative:

> These products, **like all geometry arithmetic**, are subject to
> `[R-ENC-04]`: a reader MUST treat a product exceeding 2⁶³ − 1 as a validity
> error at layer scope.

Gᵢ·Tᵢ is geometry arithmetic. Reading A requires either that it is not, which
is untenable, or that the appositive asserts nothing, which is a strained
reading of a clause placed inside a MUST.

Second, and this is what removes the reporter's principal ground, §21.1:

> The **Instances** column enumerates what a conformance corpus builds for
> that row (§21.8): the row is the rule, and each instance is one file.

L2's Instances cell is a corpus build list, not a definition of the condition's
extension. L2's *Condition* cell — "A declaration-derived sum or product of a
layer exceeds 2^63 - 1 although every contributing field is in domain" —
covers Gᵢ·Tᵢ on its face. And §21.1's "where a row and the rule it cites
diverge, the rule governs" points the same way. §4.2's parenthetical is a
gloss on "**any** quantity", and §17.2's Note reads it exactly as broad:
"`[R-ENC-04]`'s overflow rule carries no such quantifier — it binds any sum or
product a file yields".

I checked the counter-argument that §17.2's Note names only P·Q and P·Bᶜ. It
names them because they are [R-COD-07]'s subjects — the Note's whole business
is contrasting that cap's addressed-tile quantifier with [R-ENC-04]'s absence
of one — and the same sentence states [R-ENC-04]'s scope as "any sum or
product a file yields".

So the 256-byte file is rejected by every conforming implementation.
REFUTED, not byte-level, severity register-bookkeeping: the only live question
is whether L2's instance cell should name Gᵢ·Tᵢ, which is a corpus decision
that moves §21.8's 277 to 278. No normative edit is required.

## Group 10 — the partial slack total (verifier-02)

Deciding text is the reported sentence itself:

> A partial total is F less **the bytes claimed** by the claimants the walk did
> enumerate — an upper bound on the file's true slack, never an under-count

"The bytes claimed" names a set of bytes; F less a set of bytes is a set
difference, which is the union reading. §9.7 says the same of the complete
walk: "Bytes the walk does not reach are slack: the verifier **sums them**" —
it sums bytes, not claimant lengths. Reading A (sum of lengths) is an
implementer's accumulator, not a licensed reading of "the bytes claimed", and
the reporter concedes as much by describing it as what one writes first.

REFUTED, editorial at most: a parenthetical "(counted once, however many
claimants claim them)" would close the accumulator trap cheaply. Not
byte-level: verdict is reject-file under both, per the reporter's own F33
construction.

## Group 11 — [R-COD-04] and sentinel entries (adversary-01) — the second byte-level flag

The finding is well built and I spent the most search effort here. It fails
against four normative texts, any one of which decides it:

1. §19.4 step 4, [R-RDR-04]: "A valid sentinel short-circuits steps 5 and 6
   for that entry: every requested sample position of its tile reads as fill
   ... bit-exactly and with no payload I/O". The reader's algorithm is
   normative; reader B, which reports failure for coordinates in [96,100),
   violates it.
2. §13.3 [R-TYP-08]: "For every addressed tile that is not stored in the live
   generation — its index entry is the sentinel (§15.2) — a reader ... MUST
   return ... that channel's fill value at every such position."
3. §21.6, whose preamble is "These are defined behaviors, not errors. A reader
   that treats any of them as a failure is the nonconforming party", and whose
   first row is "An index entry is the sentinel | The tile is addressed but
   not stored; every sample position it carries reads as the channel's fill".
4. §15.2 [R-IDX-02]: "Sentinel entries are a reserved pattern, **not offsets
   or lengths**" — the leading clause, general, of which the [R-ENC-03] /
   [R-ENC-04] pair are the named applications. [R-COD-04] speaks of "the index
   entry's length"; a sentinel has none.

And [R-COD-04]'s own quantifier: "The stored bytes are the filtered image
verbatim. The index entry's length **therefore** MUST equal the tile's decoded
size" — the obligation is derived from there being stored bytes, and §3.1
makes an unstored tile one with none. So T14's "non-sentinel" is a faithful
restatement, not a divergence, and §21.1's rule-governs clause never fires.

Reading (a) would make the same 20 bytes simultaneously a violation and a
condition §21.6 declares not an error, and would oblige a reader both to serve
fill ([R-TYP-08]) and to reject the tile. REFUTED, not byte-level.

Severity editorial only because the cheap qualifier costs nothing and the
document adds it scrupulously elsewhere (T1, T8–T12, T14, and every structural
row of §15.3): write "a non-sentinel index entry's length" into [R-COD-04].
The reporter's implementation hazard — the rule inviting a sweep over the
whole entry array before classification — is a real hazard and the qualifier
answers it.

## Group 12 — §16.1 and structural entries (reader-03)

The reporter says settling this costs a three-rule chain. It costs one hop.
§16.1 itself points at §15.3: "A verifier MUST check the invariant (violation:
reject-layer, §15.3)". §15.3's [R-IDX-03], in the paragraph immediately above
the table, states the exclusion:

> Such an entry contributes no stored extent to the *verifier* rows, which
> bind over well-formed entries' extents only — `[R-SLB-03]`'s run continuity
> closes over it as it does over a sentinel

and §15.3's verifier rows are the two overlap rows plus "alignment or slab
invariant violated (§16)". L40's own Governing rule cell reads
"`[R-SLB-01]` (R-IDX-03)" — the register row names the deciding rule.
REFUTED, severity none. An optional cross-reference in §16.1 is a maintainer's
taste call, not a repair.

## Group 13 — §21.2's "that file's *geometry*" (register-01)

The census is right: every other use of the word means a layer's dimensional
declarations. But the passage decides its own extension in the next sentence:

> Four rows are outside that reasoning and do reach it, because their subject
> is **a field fixed across every major** (`[R-CNT-24]`)

The contrast fixes "geometry" here as "the fields a future major may redefine",
i.e. the file's structural layout, and the arithmetic closes at 32 + 4 = 36.
§2.3 fixes the verdict independently: "a file declaring another major is
neither conforming nor nonconforming under it". PARTIAL, editorial: the word
is doing unusual work and "byte layout" or "structural layout" would cost one
word.

## Group 14 — F in two senses (register-02)

Real dual use: §5.1 "the live trailer's committed file length F"; §15.3 "with
F the committed file length"; §19.1 step 1 "Obtain the transport-authoritative
file size F". The tie is [R-CNT-01]: "The file size of a conforming file
equals the live trailer's committed file length F", and §6.2 makes a reader
validate "committed_file_length equals the file size" in the same batch as the
dir bounds. Every file on which the senses diverge is reject-file under F17,
which the reporter concedes. F5's and F17's cells name both quantities
explicitly where it matters. PARTIAL, editorial: gloss F once in §21.2's
preamble, or leave it.

## Group 15 — L23's Detected tier (register-03)

Refuted by §21.1's own description of the column: "the actor obliged to detect
it (`[R-CNF-04]`, `[R-CNF-11]`), **the point by which detection is due**
(§19.2)". A deadline, not an exact point. §19.2 says the same twice: "no later
than the reader's first reliance" and "A reader MAY detect any violation
earlier (`[R-CNF-12]`)". §19.1 step 4's open-time determination is therefore
licensed and L23 understates nothing. REFUTED, severity none.

## Group 16 — Appendix A's "local reader" (diagrams-01)

§6.1 is unambiguous: "That distinction governs the request accounting of §6.4
and nothing else; the obligation over the front block turns on residency
instead ... **The test is residency, not transport**". Appendix A's sentence
picks the wrong subject — but carries the right quantifier in its own relative
clause: "which `[R-CNT-04]` requires of **any reader holding them**" — and the
two sentences after it are about residency ("bytes [0, 16) stay non-resident,
so §6.1 leaves the front-block check to the reader"). So the illustration
states the rule correctly while naming the wrong class as its subject.
PARTIAL, editorial: "A reader holding bytes [0, 16)" for "A local reader".
Not byte-level: Appendix A is non-normative and §6.1 decides.

## Group 17 — §9.6's rejected count (quiz-01)

Looked for the sentence fixing what "rejected" ranges over. The nearest is
§9.6's own opening, which makes every magic match a candidate and only some
valid:

> probe backward at 64-aligned offsets o for the trailer magic; on a match,
> require the trailer CRC to verify and committed_file_length = o + 64. The
> nearest-to-end **valid** candidate is the last committed state

"Valid candidate" presupposes invalid candidates, which are exactly the CRC and
length failures, so the reporter's reading (a) is the one the section's own
vocabulary supports. The residual doubt comes only from the reporting clause
sitting inside a sentence whose topic is re-verification failures. PARTIAL,
editorial: "how many candidates it rejected" closes it. Not byte-level —
§9.6: "no verdict turns on the probe".

---

## Groups I tried hardest to kill and failed

- Group 1 (§11.1 "last"). Five reporters, one word, and no sentence anywhere
  in the document uses "last" in the sense this passage needs. The absence is
  the evidence.
- Group 2 (§13.3's Note). I attacked it through a loose reading of
  "stored-tile set" and §3.1 shut that down; §20.4's separate supersede
  sentence and the dead "or index content" disjunct finished it.
- Group 6 (Appendix G item 5's stride claim). I looked for a reading of "every
  tile it touches" that survives and found the normative text asserting the
  identity case in §20.3 step 4.

## Groups I killed

- Group 9 (Gᵢ·Tᵢ) and Group 11 (codec-1 vs sentinel) — the round's two
  byte-level flags. Both refuted on quoted normative text, both with the
  deciding premise stated above so it can be attacked.
- Groups 10, 12, 15 — decided by a sentence the reporter did not reach or did
  not weigh.

Byte-level survivors: 0.
