# Round 12 triage — implementer-consequence lens

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full, section by section:
  front matter; §2.1–§2.5; §3.1; §4.7; §5.1–§5.2; §6.3; §7.1–§7.4; §9.1–§9.2, §9.7;
  §10.1–§10.4; §11.1–§11.3; §14.5; §15.1–§15.4; §16, §16.1–§16.2; §17.2 (codec 4),
  §17.4; §18.1–§18.2; §19.1–§19.4; §20.1–§20.5; §21.1–§21.9 (all register tables);
  §23.1–§23.2; §24; Appendices A, B, C, F, G, H.
- `ls` of the round-12 scratchpad directory. I did **not** open the reporters'
  transcripts: every claim below was checked against the specification text
  directly, and each finding's own quoted excerpt was re-verified in place.
- I did not read `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
  `spec/registry.json`, git history, or the web.

## Method

For each finding I asked my lens's question: *name the wrong thing an
implementation does.* A finding survives as byte-level only if I can describe
two implementations, both defensibly built from this text, that emit different
bytes or reach different accept/reject verdicts — and only if no sentence in
the document decides between them. Every downgrade below carries the quotation
that decides it.

---

## Group 1 — appender carries a malformed index entry into a region it authors
**members:** reader-01, writer-01, adversary-01, quiz-01
**location:** §20.3 [R-WRT-04] step 2 and step 4; §2.3 [R-CNF-05]/[R-CNF-06]; §20.1 [R-WRT-01]; §20.5 [R-WRT-06]

All four describe the same defect: §20.3 step 2 tells an appender to carry a
malformed tile-index entry forward byte-identically into a region step 4 forces
it to re-emit at a new placement, and the reconciliation the paragraph supplies
("re-emitting it byte-identically is not authorship, since `[R-WRT-05]` makes only
*a record it modifies* new output") is expressly attached to the *next* sentence,
about "any other structure", and cites a rule about records. A tile-index region
is not a record. So the collision with [R-CNF-06] ("An updater MUST satisfy every
writer requirement for the bytes it produces") is left un-reconciled. That much is
correct and I confirm it.

**But the outcome is not open.** §20.3 step 2 states this exact case and states
the action:

> "a malformed index entry an appender meets while re-emitting a region is
> carried forward byte-identically at its disk-ordinal position under step 4,
> not repaired to a sentinel"

and immediately after:

> "An appender that carries a violation forward SHOULD report it, and a caller
> that is not told cannot know the file it extended was already damaged."

"the file it extended" is past tense: the document contemplates the extension
happening. A SHOULD-report, not a MUST-refuse. And step 2's own bar rule is
exhaustive:

> "A violation the open establishes bars the commits its outcome bars and no
> others: reject-file bars every commit, and reject-layer bars a commit that
> modifies that layer."

A T8/T10/T11/T12 condition is reject-tile; nothing bars the commit. §20.5's
MUST-refuse for compactors is paired with [R-WRT-09]'s deep verification
obligation ("it relies structurally on every structure it copies, so it MUST
verify each link of the chain"), which the appender does not have —
[R-WRT-03] fixes its depth at "the §19.4 index chain for every segment whose
entries the commit reuses (`[R-IDX-04]`)", and [R-IDX-04] is crc_of_crc_array
and segment CRCs only, never §19.4 step 4's entry classification. The
asymmetry between §20.3 and §20.5 is therefore structural and deliberate, not
an oversight.

Implementer check: all four reporters independently implemented the *same*
behaviour (commit and report). There is no branch left unwritten and no byte
that differs between them. The residual defect is that the document never says
in terms that §20.3 is an exception to [R-CNF-06] for this one case, and mis-cites
[R-WRT-05] as if it could reach an index entry.

**byte-level: no.** Consensus PARTIAL. Repair: state the exception where the
general rule lives — extend [R-CNF-06] with "except where §20.3 obliges an
appender to carry an index entry forward" — and replace the [R-WRT-05]
justification for the index-entry sentence with one that reaches a re-emitted
region (the entry is preserved content, not new output, on the same footing as
a retained record).

---

## Group 2 — a commit that shrinks an extent (or changes decoded size) invalidates carried tile content
**members:** writer-02
**location:** §20.3 [R-WRT-04] step 4 and the shape-(c) example; §14.5 [R-SER-05]; §21.4 T4/T3

Verified the arithmetic: extents (8,8), tile extents (4,4) → G=(2,2), N=4, no
padding positions. Change E_x to 7: G_x = ⌈7/4⌉ = 2 still, entry_count 4 still,
extent_length unchanged ([R-CNT-17] satisfied), stored-tile set unchanged, index
content unchanged. So §20.3 step 4 forces no index re-emission and no tile
re-emission. But x = 7 is now a padding column, and [R-SER-05] is unqualified:

> "at every padding position, a writer MUST encode, for each channel the
> position carries, that channel's fill value"

The two untouched edge tiles now carry real data at a padding position: §21.4
row T4, detector verifier, tile scope. The output file is nonconforming.

The document never states what a commit owes here. `shrink`/`shrunk` appear
nowhere; every discussion of extent change is growth (§20.1 "growing extents",
step 4 "added tiles, grown extents", §11.1's rationale "grow extents as data
arrives"). The one analogous case is treated only in a **non-normative Example**
([R-CNF-01] excludes text labelled *Example*):

> "A fill change on a layer carrying either additionally requires re-emitting
> the affected stored tiles, whose content `[R-SER-05]` fixes — which makes it
> shape (b)."

I could not find a sentence that decides the extent case, and the two rules that
bear on it point opposite ways:

- against updater B: [R-WRT-01] licenses only "a violation **latent** in a
  structure they neither modify nor rely on" to travel — this one is not latent,
  it comes into existence at this commit;
- for updater B: §20.1 draws a deliberate contrast — "A creator emits only
  conforming files (`[R-CNF-05]`). An appender and a compactor satisfy every
  writer requirement for the bytes **they produce**" — and B produces no tile
  bytes at all.

Two implementations, concretely: **A** re-emits both edge tiles fill-encoded at
x = 7, re-emits the 84-byte index region re-pointing them, and a new directory —
hundreds of bytes. **B** emits a new directory, pad and trailer only. Both claim
conformance; a verifier certifies A and rejects two tiles of B under T4. B is the
branch an implementer building "resize a layer" writes by default, because the
normative step-4 list never mentions tile content. The same hole reaches any
declaration change that alters a tile's decoded size (a channel type change, a
channel-set change on an interleaved layer) → T3/[R-SER-07] on every stored tile.

**byte-level: yes.** No downgrade quotation exists. Consensus CONFIRMED.
Repair — a maintainer decision, either arm closing it:
(i) forbid the operation: state in §11.1/§20.3 that a commit MUST NOT reduce any
Eᵢ, change any Tᵢ, or change a channel's type or the channel set of a layer that
has stored tiles; or
(ii) require re-emission: add to [R-WRT-04] step 4 that a commit whose
declaration change alters what [R-SER-05]/[R-SER-07] fix for an existing stored
tile MUST re-emit every affected stored tile, and generalize the shape-(c)
example's fill sentence to say so.

---

## Group 3 — Appendix G item 2's derived file_id is not determined
**members:** writer-04, diagrams-04, adversary-03, quiz-02

Four reporters, one defect, four sub-gaps each of them found independently:
no hash named (contrast item 1's "a named codec implementation at a named
version" and item 9's "a named JSON writer at a named version"); "the trailer's
other fields" is ambiguous and, read to include the CRC at [60,64), circular
since §6.2's CRC covers [0,60) which contains file_id; no serialization of the
hash input stated; no digest→u64 reduction, byte order, or zero-substitution,
which [R-CNT-06]/F12 make necessary. Confirmed against the text: item 2 says
only "a cryptographic hash", and the claim it makes for itself — "Hashing the
bytes rather than an abstract notion of 'content' is what makes the identifier
well defined" — does not survive.

**byte-level: no**, decided by Appendix G's own preamble:

> "It adds no requirement to any actor: a writer ignoring it is fully
> conforming"

Every candidate file_id is nonzero and therefore conforming under [R-CNT-06];
no reader's or verifier's verdict moves. Consensus CONFIRMED, severity
design-decision (the maintainer must pick a hash and a serialization). Repair:
name the hash (SHA-256), define the input exactly (bytes [0, F−64) followed by
the 64-byte trailer image with [48,56) and [60,64) zeroed), fix the reduction
(first eight digest bytes little-endian) and the zero case (substitute 1).

---

## Group 4 — Appendix G item 3 ties no order between top-level records of one unassigned type
**members:** reader-02, writer-03, verifier-02, diagrams-05, adversary-05

Five reporters, one defect. Verified both halves: [R-CNT-14] bounds only layer
records (unbounded), the file-scope user-metadata record (one) and the per-layer
sub-record (one), so a conforming file may carry several top-level records of one
experimental type — §21.6 records exactly such a record as conforming. And item 3's
tie-break is textually confined:

> "Records are ordered by type, and within type 0x0001 by layer name; a layer
> record's sub-records are ordered by type, and within a type by their encoded
> bytes compared lexicographically"

The tie propagates into the placement pass ("then any record extents in ascending
record order"), so both directory bytes and extent positions are undetermined.

**byte-level: no**, decided by the same preamble sentence quoted in group 3, plus
[R-CNT-14]: "Record semantics MUST NOT depend on record order: readers MUST NOT
infer meaning from the position of a record within the sequence." Both orders are
conforming files that every reader treats identically. Consensus CONFIRMED,
severity editorial. Repair: one clause — order records within a type by their
encoded bytes compared lexicographically, at both levels.

---

## Group 5 — a profile compactor cannot satisfy both item 2 and [R-WRT-06]
**members:** writer-08

Checked the chain: item 4 fixes "One generation"; a compactor's output is
generation 1 by [R-WRT-06]; so a compactor can be a profile writer. Compacting a
file that is already compact and already item-3-placed reproduces every byte of
[0, F−64) and every other trailer field, so item 2 derives the input's own
file_id — which [R-WRT-06] forbids in terms: "It MUST mint a fresh file_id for
the output — a new draw under §9.3's randomness advice, not merely a value
compared against the input's".

**byte-level: no**, decided by that MUST plus Appendix G's "adds no requirement
to any actor" — the normative rule governs and the set of file_ids a conforming
compactor may emit is unchanged. Consensus CONFIRMED, severity editorial.
Repair: one sentence in item 2 or item 4 noting that a compactor cannot adopt
item 2, [R-WRT-06]'s fresh draw governing.

---

## Group 6 — can two MU=0/PE=0 drops license each other?
**members:** writer-05

The text forecloses the bootstrap twice in one paragraph:

> "An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to"
> "Dropping the record is not itself such a change either, so a commit whose
> only effect would be the drop MUST retain it."

The italicised *independently* is doing exactly this work, and the final sentence
exists to stop a drop from counting as its own licence. Two mutually justifying
drops are not independent of each other, and a commit whose only effects are
drops is a commit "whose only effect would be the drop". Reading (i) would make
the prohibition evadable by pairing any forbidden drop with a second one, which
is the reporter's own objection to it. **byte-level: no.** Consensus PARTIAL —
the wording is thinner than it should be for the plural case. Repair: change
"Dropping the record is not itself such a change either" to "No record's drop is
such a change".

---

## Group 7 — [R-SLB-04]'s trigger is narrower than its own scope clause
**members:** writer-06

Confirmed the mismatch: the trigger is "supersedes a stored tile in, or grows the
extents of"; the scope in the same sentence is "a run whose stored-tile set or
byte placement the commit changes". Storing a previously-sentinel tile is not
superseding (§3.1: "Superseded payload bytes from earlier generations do not make
a tile stored"), and unstoring is not either; both change a run's stored-tile set.

**byte-level: no**, decided by [R-SLB-03] binding the file independently of the
trigger — "When declared, for every run: ... the first stored tile's offset
satisfies offset mod A_slab = 0. ... A verifier MUST check these invariants
(violation: reject-layer)" — together with [R-CNF-05]. A writer reasoning from
[R-SLB-03] forward reaches the same permitted byte sequences either way; only the
route is defective, and the section's own note claims the trigger list is
complete, which it is not. Consensus CONFIRMED, severity editorial. Repair:
replace the trigger with the scope clause — "whose commit changes any run's
stored-tile set or byte placement".

---

## Group 8 — no flag source for a type the updater implements but §7.3 does not register
**members:** writer-07

Real seam: §20.4 branches on "a type §7.3 registers" versus "a type the updater
does not implement", and [R-CNT-22] says stored bits are "authoritative only for
record types the consuming tool does not implement", so an implemented private
type falls between. **byte-level: no**, decided by §10.3:

> "Experimental values are private use and carry no collision protection: two
> unrelated experiments MAY select the same value, and nothing in this format
> distinguishes them."

A private type's persistence is by construction outside what this document
decides; the silence is the design, and §20.4's opening line ("Persistence
governs every record type; only the authoritative source of the flags differs")
already obliges the implementing tool to apply *some* persistence. The
registry-assigned branch cannot arise in format major 1 — §7.3 assigns 0x0001 and
0x0002 only, and [R-EXT-05] makes "the section that defines the space" the
authority, so a future assignment updates §7.3. Consensus CONFIRMED, severity
editorial. Repair: one clause in §20.4 — for a type the updater implements that
this specification does not register, the definition the updater implements
supplies the flags.

---

## Group 9 — does "the layer's declarations" include the name?
**members:** reader-03

§19.2 is the operative timing rule and it assigns the name and the record to
different tiers in the same list:

> "**at open:** ... the directory region and its record walk, and the layer-name
> namespace (§19.1's steps);
> **at first access to a layer:** the full validation of that layer's record
> (§19.3), before any use of the layer's declarations"

So the open's use of the name is the open tier's own obligation, listed
separately from §19.3's. **byte-level: no** — and independently foreclosed by
"A reader MAY detect any violation earlier (`[R-CNF-12]`)" plus §19.2's rationale
that "divergence is only ever toward earlier rejection, never toward silent
acceptance". Every reading rejects the same layers and serves the same bytes;
only open latency moves. Consensus PARTIAL — §19.3's phrase would read better as
"the first operation using any of the layer's declarations beyond the name checked
at open". Severity editorial.

---

## Group 10 — does a reject-layer that does not block enumeration make the slack total partial?
**members:** verifier-01

Both statements of the trigger are factual, not categorical. §5.2:

> "Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection stops it, or because the verifier elected
> under `[R-CNF-11]` to stop at the first violation — the verifier MUST report
> the total as partial. A partial total is F less the bytes claimed by the
> claimants the walk did enumerate ... It is not the file's slack total but a
> bound on it, tightening to the exact total when the walk completes."

"stops it" / "blocks enumeration" is a condition, not a definition, and the
closing clause keys exactness to whether the walk completed. An L35 fill byte
stops nothing. **byte-level: no** — the file is nonconforming under either
reading and no verdict, emission, or acceptance moves; only the reported number.
Consensus PARTIAL, severity editorial. Repair: "a scope-level rejection that
prevents the verifier from enumerating that scope's claimants".

---

## Group 11 — must a verifier decode every stored tile?
**members:** verifier-03

Confirmed the delivery gap: §9.7 stops at checksums and disjointness, §17.4
frames decoding through §14's content obligations only, and Appendix H's verifier
list names only "decoded-content obligations — padding samples and interleaved
boolean bytes". T3 and T17–T25 are reachable only by decoding. **byte-level: no**,
decided by §2.3 and §2.4:

> "**Conforming verifier.** A reader that additionally checks every file-level
> requirement — including those ordinary readers are exempted from — and
> certifies conformance."
> "a verifier certifies only violation-free files"

Two implementations that read §2.4 agree on every verdict. Consensus CONFIRMED
(the derivation costs four sections), severity editorial. Repair: one clause in
§9.7 or §17.4 — a verifier decodes every stored tile.

---

## Group 12 — layout-table column sets disagree three ways
**members:** diagrams-01

Verified: front matter says five columns and omits taxonomy class; §4.7's note
says six including it; §6.1 delivers Offset|Size|Value|Class and §7.2 delivers
Offset|Size|Type|Field|Class. Also verified the second divergence — front matter
"whether the file is accepted" versus §4.7 "whether the file, layer or tile is
accepted at all". **byte-level: no**: the front-matter block is headed
"**How to read this document** *(non-normative)*", and neither passage constrains
any field's value. Consensus CONFIRMED, severity editorial. Repair: align the
front matter to §4.7's six columns and its wider acceptance clause, and either
add the missing columns to §6.1/§7.2 or have §4.7's note state the exemptions it
already states for §7.4.

---

## Group 13 — vectors cite register rows, whose numbering nothing stabilizes
**members:** diagrams-02

Verified: §2.2's stability guarantee covers `[R-<PREFIX>-<NN>]` only — "they are
never renumbered or reused, a withdrawn requirement leaves its identifier
permanently retired" — while [R-VEC-02] requires the manifest to record "the §21
register row it exercises", and §21.1 makes no promise about F/L/T/R numbering.
**byte-level: no** — a manifest citation key, and [R-VEC-01] already makes the
corpus derivative. Consensus CONFIRMED, severity register-bookkeeping. Repair:
either add a stability clause for row identifiers to §21.1, or have [R-VEC-02]
also require the row's governing requirement identifier; and fix the front
matter's claim.

---

## Group 14 — §20.4's summary omits the layer-scope user-metadata sub-record
**members:** diagrams-03

Verified §7.3: type 0x0002 is one row, MU = 0 / PE = 1, scope "file when
top-level; layer as sub-record". §20.4's rule is unhedged — "both registered
types carry PE = 1, so neither can be dropped" — and Appendix H states it
correctly ("never removes a layer record, or a user-metadata record at either
scope"). The summary sentence "No commit therefore removes a layer record or a
file-scope user-metadata record" narrows it. **byte-level: no**, decided by the
rule two paragraphs above the summary, quoted here, and by §21.1's principle that
a restatement never governs over its rule. Consensus CONFIRMED, severity
editorial. Repair: "...or a user-metadata record at either scope".

---

## Group 15 — §23.2 says a sentinel marks a tile "never stored"
**members:** diagrams-06

§3.1 is per-generation: "A tile is *stored in a generation* if and only if that
generation's tile-index entry for it is not the sentinel (§15); unqualified
*stored* means stored in the live generation", and §20.3 step 4 makes the
transition normative ("entries for tiles that become unstored written as the
sentinel"). §23.2's "never stored" is therefore wrong in the direction that
matters for a privacy inventory: §23.1 is emphatic that superseded bytes remain.
**byte-level: no** — descriptive prose; the sentinel's effects are governed by
[R-IDX-02], [R-TYP-08] and [R-LIF-08]. Consensus CONFIRMED, severity editorial.
Repair: "marks each addressed tile not stored in the live generation; a tile
unstored by a later commit leaves its payload in the file as slack (§23.1)".

---

## Group 16 — §21.9's "One does not" undercounts
**members:** diagrams-07

The paragraph names its own counter-example: "a user-metadata key at most 255
bytes by §18.2's folding of §4.6's name rules onto keys, **which carry no such
prefix**" — so the 255 does not follow from a field width, an external format
(RFC 8259 bounds no key length), or a value domain. At least two hard limits are
chosen here. **byte-level: no**, decided by §21.9's own disclaimer — "this
section collects the ones an implementer most often needs at hand, and is a
finding aid rather than an inventory — each limit is normative where the
structure forcing it is defined" — with both limits normative elsewhere
([R-SLB-01]/[R-CNT-23]; §18.2/[R-MTA-04] and row R10). Consensus CONFIRMED,
severity editorial. Repair: "Two do not: the 512 floor on A ... and the 255-byte
key bound, folded onto a namespace with no length prefix."

---

## Group 17 — §5.1's caption calls a first emission a re-emission
**members:** diagrams-08

§20.3 shape (a) is explicit — "**(a) A new layer.** Nothing existing is
rewritten." — and [R-WRT-04] step 4 keeps the paths apart: "entries new to this
generation (added tiles, grown extents) emitted per §15" versus re-emission
"necessarily at a new placement". The §5.1 caption cites the layer-B commit as an
instance of the re-emission rule, and the figure's hatched runs are, by the same
caption, "the directories, pads and trailers of commits 1 and 2" — no superseded
index region appears. **byte-level: no**: [R-WRT-04]/[R-WRT-05] decide what moves,
and placement is free under [R-SLB-05] either way. Consensus PARTIAL — the caption
conflates first emission with re-emission, but nothing in it suggests an existing
structure moves. Severity figure. Repair: "— the commit that added layer B here
emitted B's index for the first time; §20.3's shape (b) is the re-emission case."

---

## Group 18 — no worked numeric example of a layer record
**members:** diagrams-09

Verified: §4.7 promises "Every non-obvious encoding is followed by a worked
numeric example"; §7.4 gives a table and parse rules with no bytes; Appendix A
"contains no layers"; §12.3 gives one 12-byte channel entry. The document never
shows a complete layer record, a tile-index region in situ, or a directory
containing a record. **byte-level: no**, decided by §7.4: "fields are packed in
table order with no alignment or padding between them" plus the exact-parse
clause — the encoding is fully determined and the reporter built a payload from
it without guessing. Consensus CONFIRMED, severity editorial. Repair: add a
worked layer-record payload (and ideally a two-entry index region) to §7.4 or
Appendix A.

---

## Group 19 — Appendix B is missing at least two fixed constants
**members:** diagrams-10

Checked Appendix B row by row: no minimum user-metadata extent length (5, fixed
by §7.1 and cited by F22/L11) and no boolean byte encodings (0x00/0x01, fixed by
[R-TYP-07] and [R-SER-02], cited by L35/T2). Appendix B already carries the
analogous unnamed floor "Directory minimums | dir_offset ≥ 16, dir_length ≥ 4",
so its own precedent covers them; Appendix C carries identifier assignments only.
**byte-level: no**, decided by Appendix B's header: "Each is normative where it
is defined; this table is a finding aid." Consensus CONFIRMED, severity
editorial. Repair: add both rows, or narrow §4.7's "All named constants appear
once in Appendix B".

---

## Group 20 — T23 is the fifth cause-row and the only unannotated one
**members:** register-01

Verified [R-COD-07]: its statement on the point is definitional ("The stored
bytes are exactly one LZ4 block ... The LZ4 frame format is not used"), and its
only reader MUST is the 0x7E000000 decoded-size cap, which the register carries
separately as L44. [R-COD-06] by contrast does give zstd's magic check a reader
procedure, carried as T17. T13, T15, T16 and T26 all annotate themselves as
cause-rows; T23 does not. I also re-checked the reporter's unconditionality
argument and it holds: an LZ4 frame begins 04 22 4D 18; read as a block, token
0x04 means zero literals and match length 8, then a match offset of 0x4D22 =
19,746 into an empty output buffer — invalid for every tile in every file, so
T25 fires regardless. **byte-level: no**: both readings reject the same tile at
the same tier with the same outcome. Consensus CONFIRMED, severity
register-bookkeeping. Repair: annotate T23 as T13/T15/T16/T26 are, or give
[R-COD-07] the reader procedure [R-COD-06] has.

---

## Group 21 — the Instances criterion is applied in both directions
**members:** register-02

Verified all four cells. T3 (length ≠ decoded size) enumerates six; T14 (codec 1
length ≠ decoded size) reads —, though a codec-1 layer is equally interleaved,
planar numeric, or packed planar bool and equally admits longer/shorter. F33
enumerates five claimant families; F7, the same range test over the same
families, reads —. §21.1's criterion ("a row whose check ranges over a family
without the condition changing shape states that range as a single instance ...
and one whose members give the condition materially different shapes enumerates
them") does not choose between them, and T15/T25 — the two rows §21.1 names as
correct — are rows whose *construction* varies, which supports the reporter's
reading (b). **byte-level: no**: no row's outcome, detector, tier or governing
rule moves; only the corpus's file count, and [R-VEC-01] already makes the corpus
derivative. Consensus CONFIRMED, severity register-bookkeeping — and it moves
§21.8's stated totals (121/248 → 121/258 under (b)), which the maintainer must
replay rather than hand-shift. Repair: state the criterion in one direction and
rewrite T14 and F7 (or T3 and F33) to match, then recompute §21.8 and [R-VEC-03].

---

## Group 22 — verdict for a document under an experimental metadata encoding
**members:** adversary-02

The document decides this, in [R-MTA-03]:

> "Both assigned encodings are core: a conforming reader MUST be able to decode
> encoding 2 ... An encoding a reader does not implement is therefore one this
> specification does not assign, and is ignore-record (`[R-CNT-25]`)."

So a verifier meeting encoding 0x80 has no capability shortfall — it implements
everything this specification assigns. §2.3 reserves *cannot establish* for "some
requirement it is unable to check on a capability or resource ground"; there is
no such ground here, and [R-MTA-05]/[R-MTA-04] have no subject, this
specification defining no document under an unassigned encoding. §21.6 settles
the rest: "A user-metadata record declares an experimental-range (≥ 0x80)
document encoding | Ignored (ignore-record); the file is conforming", and §2.4
lets a verifier certify a violation-free file. [R-MTA-09]'s cannot-establish path
is expressly the *resource* decline on the 16 MiB bound, and §17.4's is expressly
an *assigned* codec a verifier cannot execute — neither reaches this case because
neither needs to. **byte-level: no.** Consensus REFUTED. Repair: none required;
at most a clause in §21.6's row noting that the record's unreadability leaves the
verifier nothing it is unable to check.

---

## Group 23 — [R-CNT-13]'s overlap branches omit two structures of one non-layer scope
**members:** adversary-04

Confirmed the gap: "a verifier MUST treat an intra-layer overlap ... as
reject-layer, and any overlap across layers or touching another scope's
structures as reject-file" enumerates neither branch for two top-level records
overlapping each other. **byte-level: no**, decided in two places: F33's head
clause reaches it — "A byte of the live committed state is claimed by two
structures that do not belong to the same layer" is true of two structures
belonging to no layer — and [R-CNF-08] supplies the class independently ("file →
reject-file"), with [R-CNT-02] making it a violation at all ("a file whose live
state does not partition this way is not a conforming file"). Readers are
expressly not obliged to detect overlap. Consensus CONFIRMED (the enumeration is
incomplete), severity editorial. Repair: "...and any other overlap — across
layers, touching another scope's structures, or between two structures of one
non-layer scope — as reject-file", and drop F33's narrowing gloss.

---

## Group 24 — is version_minor still the only descriptive field?
**members:** quiz-03

§4.7's class test is the four-item gloss, not the bare word "anything":

> "A field is **structural** if its value determines anything a conforming
> reader or verifier does with the file's bytes — where a byte lies, how it
> decodes, what a decoded value is, or whether the file, layer or tile is
> accepted at all, which is the sense `[R-CNT-07]`, `[R-MTA-02]` and
> `[R-SEC-06]` already use."

A compactor propagating the input's minor into its output ([R-WRT-06]) does none
of those four with the file's bytes: no byte moves, nothing decodes differently,
no value changes, nothing is accepted or rejected — [R-CNT-07] forbids gating on
it in terms ("A reader MUST NOT reject a file for its version_minor"). So
version_minor stays descriptive. **byte-level: no**: [R-WRT-06] states the
compactor's output minor explicitly and [R-CNT-07] the reader rule, so both the
bytes and the verdict are decided whichever label is used. Consensus PARTIAL —
the surface tension with §2.3's "updaters are readers" is real. Severity
editorial. Repair: scope §4.7's descriptive clause to a reader's read path, or
note that a writer-side propagation rule does not make a field structural.

---

## Coverage

34 input ids, 24 groups, each id in exactly one group; counted twice by hand
against the input list. One group upheld as byte-level (group 2, writer-02).
No finding was left unevaluated.
