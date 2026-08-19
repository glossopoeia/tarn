# Round 12 triage — correctness lens — working transcript

## What I read

Only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, via `sed`/`awk`/`grep`
over these regions:

- front matter (lines 1–40), §2.2–§2.5 (116–300), §3.1 terms (300–306)
- §4.7 field taxonomy + note (500–535)
- §5.1 anatomy incl. the three-commit figure (571–600), §5.2 coverage / `[R-CNT-21]` (600–660)
- §6.1 front block table (655–700)
- §7.1 (840–866), §7.2 framing + `[R-CNT-12]`–`[R-CNT-15]` (867–948), §7.3 registry (949–968), §7.4 layer record (969–1030)
- §9.7 coverage walk `[R-LIF-08]`
- §10.1–§10.4 extension surface / experimental range
- §11.1–§11.2 geometry, §12.3 channel-entry example (1580–1600), §13/§15 notes (1680–1710)
- §14.5 padding content `[R-SER-05]`
- §15.1–§15.3 index layout, sentinel, entry validity
- §16.2 slab `[R-SLB-02]`–`[R-SLB-04]`
- §17.2 codecs 1–4 + `[R-COD-08]`, §17.4 `[R-COD-11]`
- §18.2 `[R-MTA-03]`, `[R-MTA-09]`, `[R-MTA-04]`, `[R-MTA-05]`, §18.3
- §19.1–§19.4 in full, §20.1–§20.5 in full
- §21.1–§21.9 in full (register rows F1–F36, L11–L44 spot-checked, T1–T26, R1–R10, §21.6, §21.7)
- §23.2, §24 `[R-VEC-01]`–`[R-VEC-04]`, Appendix A, Appendix B, Appendix G items 1–10, Appendix H

I did not read the round-12 reporter transcripts, `docs/`, `PLAN.md`, `AGENTS.md`,
`conformance/`, `spec/registry.json`, or git history. Every quotation below was
re-read in the document rather than taken from a finding.

## Grouping

34 input ids → 24 groups. Three multi-reporter groups:

1. `appender-carries-malformed-index-entry` — reader-01, writer-01, adversary-01, quiz-01
2. `profile-top-level-record-order` — reader-02, writer-03, verifier-02, diagrams-05, adversary-05
3. `profile-file-id-underspecified` — writer-04, diagrams-04, adversary-03, quiz-02

The remaining 21 ids are each a distinct defect. writer-08 is *not* merged into
group 3: it is a collision between item 2 and `[R-WRT-06]`, not the
under-specification of item 2. writer-02 is *not* merged into group 1: group 1 is
about a violation latent in the input; writer-02 is about a violation the commit
itself creates. adversary-05, diagrams-05, verifier-02, writer-03 and reader-02 all
name the same missing tie-break in Appendix G item 3 and are one group even though
two of them also mention the extent-placement consequence.

## Group 1 — the appender carry-forward (4 reporters, all self-flagged byte-level)

Claim: §20.3 step 2 orders an appender to write a malformed index entry into a
tile-index region it is newly authoring, which `[R-CNF-05]`/`[R-CNF-06]` forbid; so
either it commits a nonconforming file or it must refuse, as §20.5 makes a
compactor do.

What the document actually says, checked line by line (§20.3 step 2, lines 2789–2803):

> "A violation the open establishes bars the commits its outcome bars and no
> others: reject-file bars every commit, and reject-layer bars a commit that
> modifies that layer. The open establishes no tile-scope violation — it consumes
> the trailer and directory only (`[R-RDR-01]`) — and a malformed index entry an
> appender meets while re-emitting a region is carried forward byte-identically at
> its disk-ordinal position under step 4, not repaired to a sentinel. … An appender
> that carries a violation forward SHOULD report it, and a caller that is not told
> cannot know the file it extended was already damaged."

Three things decide the outcome:

- "**bars the commits its outcome bars and no others**" — an exhaustive barring
  rule, and a tile-scope outcome bars nothing.
- "**is carried forward byte-identically at its disk-ordinal position under step
  4**" — step 4 is executed, i.e. the commit proceeds. Under the reporters'
  reading (b) this sentence could never operate in the one case it names.
- "**a caller that is not told cannot know the file it extended was already
  damaged**" — the extension completed.

And §20.1 `[R-WRT-01]` (lines 2743–2751) assigns whole-file conformance away from
the appender in terms:

> "A creator emits only conforming files (`[R-CNF-05]`). An appender and a
> compactor satisfy every writer requirement for the bytes they produce and the
> preservation obligations of §20.4 for what they carry forward (`[R-CNF-06]`) …
> **certifying the whole file is a verifier's office (§9.7)**."

The compactor asymmetry the reporters lean on is explained rather than
contradicted: `[R-WRT-09]` gives the compactor a verification depth that reaches
"each retained layer's … full index chain … and each relocated extent's checksum,
including every stored tile's entry crc", whereas `[R-WRT-03]` gives the appender
only "the §19.4 index chain for every segment whose entries the commit reuses" —
§19.4 step 3 (`[R-IDX-04]`, CRCs), not step 4 (`[R-IDX-03]`, classification). And
§20.5's prohibition is expressly conditioned on detection: "MUST NOT emit a file
carrying a violation **it has detected**". Two tiers, two depths, two rules.

So reading (b) is not permitted by the words. But the reporters found something
real underneath: the *grounds* §20.3 gives are wrong for the case it gives them for.

- "`[R-LIF-01]` freezes the committed prefix" is offered as the reason repair is
  barred, but §20.3 step 4 puts the re-emitted region at and after F, which
  `[R-LIF-01]` does not freeze. (writer-01 and quiz-01 both spot this.)
- "re-emitting it byte-identically is not authorship, since `[R-WRT-05]` makes only
  *a record it modifies* new output" cites a rule about records. `[R-WRT-05]` reads
  "every record it retains and does not logically modify — header, inline payload,
  and extent slot"; a tile-index region is not a record, and §15.1 puts the entry's
  owning scope at the tile. The carve-out is also expressly scoped to "any **other**
  structure the appender carries forward", i.e. not the entry.

The real reason repair is barred is unstated: re-pointing the entry to a sentinel
would change what the layer denotes (`[R-MDL-02]`), and the appender's obligation
runs to the bytes it produces, not to the file's certification. Grade PARTIAL,
byte_level false.

## Group 2 — Appendix G item 3, top-level same-type records

Verified: `[R-CNT-14]` (line 924) — "multiplicity rules are per type — in format
major 1: any number of layer records …; at most one file-scope user-metadata
record …; and at most one user-metadata sub-record per layer record." Nothing
bounds an unassigned type. §21.6 records an experimental-range MU = 0 record as a
non-violation. Item 3 reads "Records are ordered by type, and within type 0x0001 by
layer name; **a layer record's sub-records** are ordered by type, and within a type
by their encoded bytes compared lexicographically". The tie-break is textually
confined to sub-records. Hole is real, at both the directory bytes and the
"record extents in ascending record order" placement pass.

Not byte-level. Appendix G's own words: "It adds no requirement to any actor: a
writer ignoring it is fully conforming." Both orders yield conforming files;
`[R-CNT-14]`: "Record semantics MUST NOT depend on record order."

## Group 3 — Appendix G item 2, derived file_id

Re-read item 2. Confirmed all four gaps: no named hash (contrast item 1's "a named
codec implementation at a named version" and item 9's "a named JSON writer at a
named version"); "the trailer's other fields" leaves the trailer CRC at [60,64)
ambiguous, and the CRC is a function of file_id; no serialization of "other fields"
into a byte string; no digest→u64 reduction and no rule for a zero result, which
`[R-CNT-06]`/F12 forbid. Item 2's own claim — "Hashing the bytes rather than an
abstract notion of 'content' is what makes the identifier well defined" — is
therefore not delivered. Not byte-level, same non-normativity quote.

## Singleton judgements (the ones where I moved a reporter's grade)

**reader-03** — §19.2's bullets decide it: "**at open:** … and the layer-name
namespace (§19.1's steps); **at first access to a layer:** the full validation of
that layer's record (§19.3)". The open's use of the name is assigned to the open
tier expressly, so §19.3's gloss cannot collapse the tiers. Real residue: the gloss
should exclude the name. PARTIAL, editorial.

**writer-02** — the shrink case. §20.3's shape (c) does not classify it: its own
enumeration is "clearing a slab declaration, renaming a layer, or changing a
channel's fill value on a layer with no padding position and no pad bit". And the
doctrine is stated on a general ground: "A fill change on a layer carrying either
additionally requires re-emitting the affected stored tiles, **whose content
`[R-SER-05]` fixes** — which makes it shape (b)." `[R-SER-05]` equally fixes the
content of positions a shrink turns into padding. `[R-WRT-01]`'s travel licence
reaches only "a violation **latent** in a structure they neither modify nor rely
on" — a violation the commit creates is not latent. So reading (ii) is not
available; the gap is that the case is never named. PARTIAL, not byte-level.

**writer-05** — the bootstrap. The italicised word decides it: "An appender may
drop it only in a commit that *independently* changes the scope the record attaches
to", closed by "Dropping the record is not itself such a change either, so a commit
whose only effect would be the drop MUST retain it." Two mutually-licensing drops
are not independent changes, and a commit whose only effects are drops has no
independent change at all. Residue: the exclusion names only the record's own drop.
PARTIAL, not byte-level.

**writer-06** — trigger vs scope confirmed at line 2080: "A writer or updater whose
commit supersedes a stored tile in, or grows the extents of, a slab-declared layer
MUST either re-establish the invariants for every affected run — a run whose
stored-tile set or byte placement the commit changes — or clear the declaration".
§3.1: "Superseded payload bytes from earlier generations do not make a tile
stored", so first-storing a sentinel tile is not superseding; §15.3 and `[R-SLB-03]`
make sentinels transparent, so unstoring promotes a run's first stored tile.
Neither is in the trigger. Outcome still decided: `[R-SLB-03]` is a validity
invariant a verifier MUST check, and the offsets it reads live in the index region
the commit re-emits, i.e. in bytes `[R-CNF-06]` binds. CONFIRMED, not byte-level.

**writer-07** — §20.4's dichotomy confirmed: "For a type §7.3 registers …" / "For a
type the updater does not implement …". Not complements. But §10.3 hands private
semantics to the private user, and `[R-CNT-22]` ("Stored flag bits are
authoritative only for record types the consuming tool does not implement") already
says the stored bits are *not* the source for an implemented type. For the registry
branch, `[R-EXT-05]` makes the defining section govern and §7.3 is that section, so
a later assignment lands in §7.3 by construction. PARTIAL, editorial.

**verifier-01** — the document leans toward reading A, not B. §9.7 names the causes
of an incomplete walk as "a scope-level rejection blocks enumeration, or the
verifier stops at the first violation", and then makes an explicit contrast for the
tile-scope case only: "An entry `[R-IDX-03]` classifies reject-tile on a
*structural* ground **does not make the walk incomplete**: the walk passes over
it". A contrast drawn for tile scope and withheld for layer scope reads as
deliberate. `[R-CNT-21]` repeats the same causal gloss. So the reporter implemented
the weaker reading. Still a MUST with two readings and a reported number that
forks. PARTIAL, design-decision, not byte-level.

**verifier-03** — resolved by `[R-CNF-12]` in terms: "A file is conforming only if
it satisfies every requirement at every scope … and **a verifier certifies only
violation-free files**", plus §2.3's "checks every file-level requirement —
including those ordinary readers are exempted from". CONFIRMED as an observation
about where the obligation is stated, not byte-level.

**adversary-02** — §21.6 and `[R-EXT-03]` foreclose rejection: "Ignored
(ignore-record); the file is conforming". `[R-MTA-09]`'s cannot-establish clause is
expressly about the size bound ("A **verifier** that declines to decode a document
on the bound above"), and §17.4's is about executing a codec, which §17.4 itself
notes arises only at a value that is already a layer-scope violation. So the
unimplemented-metadata-encoding case is genuinely unaddressed, and `[R-CNF-11]`'s
general criterion ("unable to check on a capability or resource ground") points to
*cannot establish* while §21.7's no-witness reasoning points to certification —
§21.7 does not reach it, since a witness exists and only the capability is missing.
CONFIRMED. Not byte-level under the stated test: both verifiers hold the file
conforming, no writer's output moves, and no reader accepts or rejects differently.
This is the closest call among the unflagged findings and I say so.

**adversary-04** — `[R-CNT-13]`'s enumeration confirmed: "an intra-layer overlap …
as reject-layer, and any overlap across layers or touching another scope's
structures as reject-file". Two file-scope structures overlapping each other are in
neither branch. F33's head clause does reach them — "claimed by two structures that
do not belong to the same layer" — and gives reject-file, which is also what
`[R-CNF-08]` gives for a file-scope owning scope. Decided; the rule's enumeration is
incomplete. CONFIRMED, editorial.

**register-01** — `[R-COD-07]` re-read in full. Its only reader obligation is "a
reader MUST treat such a declaration as a validity error at layer scope" (the
0x7E000000 cap, = L44). Nothing in it gives a reader procedure for the frame magic,
unlike `[R-COD-06]`, which does and is carried as T17. T23 is a fifth cause row and
is the only one without the annotation T13/T15/T16/T26 all carry. Detection is
`[R-COD-08]`'s (T25). CONFIRMED, register-bookkeeping, not byte-level.

**register-02** — §21.1's criterion re-read. T3 enumerates six (three decoded-size
formulas × longer/shorter); T14, the same comparison under codec 1, enumerates one.
F33 enumerates five claimant families; F7, a range test over the same families,
enumerates one. The criterion is applied in opposite directions. Totals are not
affected. CONFIRMED, register-bookkeeping.

**quiz-03** — §4.7's structural test is glossed by an exhaustive-looking
enumeration: "determines anything a conforming reader or verifier does with the
file's bytes — **where a byte lies, how it decodes, what a decoded value is, or
whether the file, layer or tile is accepted at all**, which is the sense
`[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use." A compactor copying the
input's minor forward does none of those. Reading (ii) survives only on the general
clause read without its gloss. PARTIAL, editorial.

**diagrams-01, -02, -03, -06, -07, -08, -09, -10** — each checked against the cited
text and each accurate as reported; all editorial/figure, none byte-level. Details
in the structured output.

## Coverage check

Counted by hand and by list: 4 + 5 + 4 + 21 singletons = 34 member ids, each input
id in exactly one group, no duplicates.
