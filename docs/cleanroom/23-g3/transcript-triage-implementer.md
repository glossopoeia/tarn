# Round 23 triage — implementer-consequence lens

## Access log

Read `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` only — §§2.1–2.5, 3.1,
4.6, 4.7, 5.1, 5.2, 6.1–6.4, 7.1–7.4, 8.1–8.2, 9.1–9.4, 9.7, 10.1–10.4, 12.2, 15.3,
15.4, 17.2–17.4, 18.1–18.3, 19.1–19.4, 20.1–20.5, 21.1–21.9, 22.3, 24.

Read **no** walk transcript and **no** `transcript-triage-*.md`. Did not list the round23
directory contents beyond the one `ls` at session start, which printed file names only;
I opened none of them. (The `ls` output showed `transcript-triage-*` files were not yet
present; no triage transcript was opened at any point.)

Ran one script over the spec: mechanical instance count of §21.2–§21.5 (semicolon-separated
cells, `—` = 1). Result: 36/49/26/10 rows = 121; 58/116/55/48 = **277** instances. This
independently reproduces §21.8's stated figure and quiz-02's arithmetic.

## Grouping

19 ids → 17 groups. Three findings land on the *same sentence* of §21.7 (the §20.3-step-4
clause) but are three distinct defects with three distinct repairs, so they get three
groups: diagrams-01 (a class omitted), adversary-03 (a witness overclaimed), quiz-01 (the
"only" mis-scoped). diagrams-01 mentions quiz-01's point as a rider; I grouped on each
finding's headline defect. reader-02 is a fourth, separate §21.7 defect (a different
sentence, about §20.5's trailer obligations).

reader-01 + adversary-04 merged: both are "§21.9 names no bound on a stored extent's
length, and [R-ERR-04] bars a within-table resource decline." adversary-04 adds the
composition point (rows multiply, 2.8e14 index entries); reader-01 adds the metadata-extent
half and the §17.2 pointer. Same defect, same repair site.

reader-03 + adversary-01 merged: both are §18.2's content-size sentence — whether the
constraint is checkable without decoding, whether "the bytes decode" is true, and whether
the declared size may be consulted pre-decode. One sentence, one repair.

adversary-02 (JSON depth) kept **separate** from group 1 even though both are "§21.9 bounds
no such quantity": the repairs differ (a depth row vs. a stored-length row), and adversary-02
is the batch's only byte-level flag — fusing it into a bigger group would bury it.

register-01 (R8 count) kept separate from quiz-02 (the 277 total is hard to check): if R8
gains two instances the total becomes 279, so they interact, but they are different defects
with different repairs.

## Byte-level judgements, with the sentence that decides each downgrade

**adversary-02 — JSON nesting depth (the one self-flagged byte-level finding).**
Verified the reporter's file is conforming: RFC 8259's grammar bounds no depth, the document
is an object, no BOM, one finite number, one 1-byte key per object, each object has one
member so [R-MTA-05]'s sort is trivially satisfied, and no §21.9 quantity is exceeded.
Verified §21.9 has no depth row and [R-ERR-05]'s hard-limit list has none.

What decides it: §18.2 [R-MTA-09], "a document exceeding that bound is **ignore-record like
any other it cannot read**". That phrase is an open licence: a document a reader cannot read
takes ignore-record. A recursive-descent reader that blows its stack on 200,000 levels
cannot read this document, so it takes ignore-record — and §2.4 fixes what ignore-record
costs: "The record is skipped as though absent. **Decoding of all stored data is
unaffected.**" [R-MTA-02] closes the rest: "A reader MUST NOT let any part of a user-metadata
document affect how a byte is located, decoded, or returned."

So both of the reporter's implementations *accept* the file, serve identical sample bytes,
and leave it conforming ([R-CNF-02], a pure predicate on bytes, is unmoved). The verifier
split the reporter names — certify vs. cannot-establish — is a split §2.3 already licenses
by design for capability grounds ("as when" introduces its list, not a closed enumeration;
the codec case [R-COD-11] is the same shape). The reporter's R7 branch is not a permitted
reading but an implementation error: the document *is* well-formed JSON.

The two premises my downgrade rests on, stated so they can be attacked:
- **P1.** "Accept or reject" in the gate is the *file*-level decision. Whether an
  ignore-record record's content reaches the application is not an accept/reject fork.
  Attack surface: ignore-record is one of §2.4's four outcome classes, and outcome class is
  exactly what a corpus manifest records ([R-VEC-02]). If the maintainer reads outcome-class
  divergence on a *conforming* file as byte-level, this flips.
- **P2.** A verifier's certify/cannot-establish split is report-level. Attack surface: this
  is the one group where the file is *conforming* and one verifier certifies it while
  another may not — unlike adversary-01 and verifier-01, where neither certifies.

**Group 1 (reader-01 + adversary-04) — stored length unbounded.** Not ambiguous; determined,
and determined against the implementer. [R-ERR-04]: "Software that declines **on that ground**
a file whose every quantity lies within the table is not a conforming reader (`[R-CNF-03]`)",
with [R-CNF-10]: "MUST accept any conforming file within the minimum guarantees stated in
§21's limits table". A reader that caps per-tile fetch is nonconforming; a reader that does
not is unbounded. No fork *between conforming implementations*, so no byte fork — but the
cost is that the conforming set may be empty in practice for the tile half. §17.2's Note
confirms the premise: "no bound relates a stored length to its decoded size in either
direction" and "Resource limits are §21's subject" — and §21 has no such row.

**Group 2 (reader-03 + adversary-01) — content size.** Both routings (R3 and R4) carry
reader detector, extent-use tier, ignore-record outcome, and both make the file
nonconforming, so no reader's service and no file verdict moves. adversary-01's Reading B
ends in "cannot establish that document's conformance and MUST NOT certify the file"
(§18.2); Reading A ends in nonconforming. Neither certifies. §2.3: "*Cannot establish* is
not a finding that the file is nonconforming, and a verifier MUST NOT certify a file it
reports that way." Same non-certifying destination, different label.
The substantive finding survives: §18.2's "the bytes decode" is a claim about decoder
behaviour, and adversary-01's run of the reference decoder (`Decoding error (36)`) is
evidence against it in both directions of mismatch — a compliant zstd decoder errors on an
FCS that disagrees with produced output. The routing rationale is therefore false as
written even though the routing costs nothing.

**writer-01 — compactor and [R-LIF-02].** §6.2: "a longer gap is conforming, and no
conforming commit produces one", and §2.3: "§6.2's pre-trailer gap longer than
`[R-LIF-02]` step 5's pad are the cases this text states" — expressly declared not a
file-conformance violation. So both compactors emit conforming files, every reader accepts
both, a verifier certifies both. The reporter's own "one row of my byte-divergence
catalogue" is the row the document has already decided is conduct, not bytes. The gap in
§20.5 is real (I confirmed §20.2 and §20.3 step 6 cite [R-LIF-02] by name and §20.5 does
not), and the durability half is a genuine safety hole, but durability is not bytes.

**verifier-01 — 128-byte floor.** PARTIAL. §21.2's preamble is not silent about F5; it
states a *rule*, not just an exception list: "the rows below whose subject is that file's
*geometry* do not reach it", with four named exceptions "whose subject is a field fixed
across every major". F5's subject is the file's size — geometry — and F5 is not among the
four, so the preamble decides F5 does not reach a foreign-major file. §2.3 backs it: such a
file "is neither conforming nor nonconforming under it". Both readings still reject the
file at the reader ([R-CNT-07]), so nothing byte-level. What survives is a genuine ordering
gap: [R-CNT-27] appears in neither half of §6.2's enumerated order nor in §19.1's four
steps, and for F < 64 the trailer checks are not even performable, so the repair has to
handle sub-64-byte files as well as the reporter's 96-byte one.

**register-02 — R6's governing cell.** PARTIAL. The reporter's load-bearing claim is that
"[R-ENC-12] expressly excludes document keys from its own scope". It does not. §4.6:
"**Names** — the strings that identify layers, dimensions, channels, **and user-metadata
keys** — satisfy three further constraints", and the carve-out that follows removes only
the *outcome* ("a validity error at the owning scope — except for a key inside a
user-metadata document, where `[R-CNT-25]`'s quarantine governs and the outcome is
ignore-record"). So [R-ENC-12] does define R6's condition, and R6 cites it in parentheses;
§21.1's tie-break does not resolve to nothing. The residual defect is real and narrow: two
rows drawn from one sentence of [R-MTA-04] name different requirements first, and per
§21.1 the first name should be "the requirement that defines it".

## What an implementation actually does wrong, group by group

- G1: fetches and CRCs an unbounded per-tile extent, or ships a cap and is formally
  nonconforming. Two teams: one streams 3 GB per tile read; one refuses at 1 GB and fails
  any corpus vector above its cap. The document sides with the first.
- G2: metadata decode wired to a whole-buffer zstd API cannot obtain R4's comparand at all
  and silently establishes nothing; a streaming reader files the same file under R3.
- G3/G4/G5/G6: nothing. Every register row is binding on the reader through [R-CNF-04]
  regardless of what §21.7 says about it. The cost lands on a corpus builder who tries to
  construct a vector §21.7 promised was constructible, and on a verifier author's mental
  model.
- G7: a compactor with one fsync at the end. Its output is byte-conforming and can be swapped
  over a good input with payloads not durable.
- G8: a 96-byte foreign-major file reported as "corrupt" rather than "format major 7",
  against §6.3's SHOULD.
- G9: a certificate loud about a 40-byte metadata extent and silent about a 96-byte
  unassigned-type extent covered by no checksum at all.
- G10: ten register rows exercised only by vectors that cannot tell scoped refusal from
  whole-file rejection.
- G11/G16/G17: navigation cost only.
- G12: an implementation whose JSON parser rejects `NaN` for free but converts `1e400` to
  +Infinity passes R8's coverage while violating [R-MTA-04]. That is the sharpest practical
  consequence in the bookkeeping set.
- G13/G14: a vector identifier that does not name the clause it tests; a reader of §20.5
  who takes (F36, L25, R1) for the whole set.
- G15: one team's reader surfaces a deep metadata document, another's reports it unreadable.
  Both accept the file; both are defensible readers.

## Mechanical check

Instance count reproduced: 277 over 121 rows. R8 = 2 instances as written; R9 and R10 also
2, but those are single predicates, so R8 is the only §21.5 row whose stated disjunction is
not enumerated. register-01's 279 follows if R8 goes to 4.
