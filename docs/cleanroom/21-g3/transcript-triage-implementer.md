# Round 21 triage — implementer-consequence pass

## Disclosure

Read: `spec/tarn.md` only — §§1–5, 6.1–6.4, 7.1–7.4, 9.7, 11.1–11.4, 13.3,
14.1–14.5, 15.3–15.4, 16, 17.2–17.4, 18.2, 19.2–19.4, 20.3 (step 4),
20.4, 20.5, 21.1–21.9, 24, Appendix F, Appendix G, Appendix H, §4.7.
Ran: `grep`/`awk` over §21.1–§21.6 to confirm no terminal requirement
identifier appears there (only `[R-ERR-01]` in §21.7 and `[R-ERR-02]`
in §21.8). Opened **no** walk transcript and **no** `transcript-triage-*`
file. Did not read docs/, PLAN.md, AGENTS.md, conformance/,
spec/registry.json, git history, or the web.

I could not consult RFC 8878 (access rule), which is the named
contingency on adversary-01. Every other finding was evaluated.

## Grouping

Every finding is a distinct defect at a distinct location. 21 findings,
21 groups. Near-collisions I checked and rejected as merges:

- **verifier-02 vs quiz-01** — same sentence-pair in [R-MTA-09], but
  verifier-02 is "this SHOULD states no consequence" and quiz-01 is
  "'the bound above' has two candidate referents". Different clauses,
  different repairs.
- **writer-03 vs quiz-03** — both concern the bound-decline on a
  user-metadata document. writer-03: §21.5's signpost claims §21.6
  lists this non-violation and §21.6 does not. quiz-03: [R-MTA-09]'s
  keywordless "is ignore-record" against [R-ERR-04]'s MAY. Different
  sentences, different failure modes; a single §21.6 entry would help
  both but is not the whole repair for either.
- **diagrams-01 vs quiz-02** — both on §2.3's acceptance duty and the
  MU = 1 carve-out, but in opposite directions (Appendix H drops the
  carve-out; §2.3's own carve-out is too wide). Different locations.
- **writer-01 vs quiz-03** — both §21.9 guarantees + reader decline,
  but different rows (tile decoded size vs document decoded size) and
  different questions (does the quantity exist vs. what force the
  outcome carries).

## Byte-level judgements

### UPHELD: writer-01 (empty layer vs §21.9's per-tile guarantee)

Test applied: does a conforming reader **MUST-accept** this byte
sequence's layer?

- Reading A (must accept): the layer addresses no tile (§11.2), and
  §3.1 defines a tile as "the unit a tile-index entry addresses", so
  the file carries no quantity "decoded size of one tile" and
  [R-ERR-04]'s "Software that declines **on that ground** a file whose
  every quantity lies within the table is not a conforming reader"
  bites. Reinforced by [R-GEO-02]: "Readers MUST accept such a layer,
  and a read of any region of it returns no samples," and §19.4 step 1:
  "any region of a zero-extent layer, succeeds and returns no samples."
- Reading B (may decline): [R-SER-07] — "decoded size is a function of
  the layer's declarations alone" — makes the 2048 MiB a real derived
  quantity, §19.3 obliges the reader to derive it at layer access ("the
  decoded sizes §14 derives from it (`[R-SER-02]`, `[R-SER-07]`)"), and
  §17.2's Note confirms it is computed in an empty layer. [R-ERR-04]
  then licenses declining "at the narrowest scope whose **declarations**
  exceed what it can serve, a layer or a tile."

Neither premise survives as forced. §17.2's Note draws the
addressed-tile quantifier **explicitly** for [R-COD-07] and **expressly
denies** it for [R-ENC-04] ("P·Q and P·Bᶜ are checked in an empty layer
even though this cap is not"); §20.3 step 4 repeats it ("which an empty
layer escapes only because that cap is quantified over addressed
tiles"). The third member of the family — §21.9's row — is nowhere
quantified. Two explicit sibling rulings and a silence is the signature
of an unresolved case, not of a settled one.

Concrete divergence, both realistic:
- Reader X computes the decoded tile size at §19.3 (which it is
  obliged to compute anyway, for [R-ENC-04]), compares against a
  256 MiB budget, and refuses the layer with a resource-limit report.
  Every read of that layer fails. This is the fail-fast implementation.
- Reader Y accepts; every read returns zero samples successfully.

Same conforming ~1 KiB file, opposite service verdicts at layer scope,
and [R-ERR-04]'s final sentence makes exactly one of them a conforming
reader without saying which.

**Correction to the reporter's writer-side story.** writer-01 says the
choice "is not recoverable, because §20.3 step 4 bars changing tile
extents once any tile is stored." §20.3 step 4 in fact says: "A layer
that stores no tile **in the generation this commit supersedes** MAY be
re-declared freely, which is what schema-first creation needs (§11.1)."
So a schema-first writer is *not* locked at creation — it can fix the
tile shape at the commit that first stores a tile. The writer-side
consequence is therefore much weaker than reported. The reader-side
fork stands on its own and is what carries this finding.

### UPHELD (with a named contingency): adversary-01 (document FCS)

§18.2 enumerates a **closed** set of carried-over frame constraints:
"under the frame constraints of `[R-COD-06]` that do not reference a
tile: the frame magic; no skippable frame and no second frame; no
nonzero dictionary ID; no content-checksum flag." R4's Instances cell
matches that set exactly, plus "bytes remaining after the frame". The
FCS constraint of [R-COD-06] — "when present it MUST equal the tile's
decoded size" — is one of "the constraints §17.2 states against a
tile's declared decoded size" that §18.2 says "do not apply". So TARN
imposes nothing on a document frame's FCS.

The document then resolves the *neighbouring* case in terms and does
not resolve this one: the window bound is "the reader's capability, not
a failure to decode within the meaning of R3". FCS gets no such
sentence, so whether an inconsistent FCS makes the bytes "fail to
decode under its declared assigned encoding" (R3) is left to the
binding.

That the document is alert to exactly this hazard is shown by §17.2's
own Note: "Whole-buffer zstd decoders that tolerate concatenated or
skippable frames do not by themselves enforce the exactly-one-frame
rule" — i.e. it pins constraints precisely so implementations do not
depend on their decoder's strictness. It pinned FCS for tiles (T22). It
did not for documents.

Divergence: Verifier A (binding that errors on FCS/content mismatch —
the reference implementation's ordinary behaviour) reports R3,
ignore-record, verdict *nonconforming*. Verifier B (streams to
end-of-frame without comparing) certifies. On a frame carrying a
Window_Descriptor, the window decline does not intervene. Exactly one
is right; this document does not say which.

**Contingency, stated so a maintainer can close it:** if RFC 8878
itself makes a frame whose present Frame_Content_Size differs from the
actual decompressed length a *malformed frame*, then "fails to decode"
is determined by a pinned normative reference (Appendix F), Verifier B
has a bug rather than a licence, and this drops to editorial — one
sentence noting the asymmetry. I could not check RFC 8878 under this
round's access rule and I am not asserting either way. The cheap repair
does not depend on the answer: state in §18.2 either that a present FCS
MUST equal the document's actual decoded length (with a row beside R4),
or that a mismatch is not a failure to decode within the meaning of R3 —
the same move §18.2 already makes for the window.

## Downgrades, with the deciding text quoted

### verifier-01 — [R-CNT-21] partial totals and F33/F7 → PARTIAL, editorial

The reporter says the rule is "stated over all scopes but written only
for layers, leaving F33/F7 open". F33/F7 are not open. [R-LIF-08]
supplies the operative test in §9.7: "Where the walk does not
complete — **a scope-level rejection blocks enumeration**, or the
verifier stops at the first violation (`[R-CNF-11]`) — the sum is
reported as partial." An F33 or F7 established *by* the completed walk
blocks no enumeration. §21.6's slack row says the same: reported as a
partial total "**where its walk did not complete**". §5.2's Note
agrees: "A partial total (`[R-CNT-21]`) reports what one verifier's
**incomplete** walk left unclaimed."

So reading (B) — 640 bytes of slack on a 640-byte file — is foreclosed,
and (A) and (C) differ only in a report label. Implementer
consequence: none to bytes, none to verdict (nonconforming under every
reading). The looseness in "a scope-level rejection" read over file
scope is real prose slack; the outcome is not open.

### verifier-02 — SHOULD with no consequence → CONFIRMED, editorial

Verified: §2.1's Note states the discipline; [R-MTA-09]'s clause "the
verifier SHOULD report the bound it applied and the stored length of the
extent it declined" is followed immediately by "The decline presupposes
an encoding this specification assigns" — subject change, no
consequence. Downgrade rests on [R-CNF-12]: "§21's register enumerates
MUST-level conditions only, and a verifier reports a SHOULD deviation as
an advisory that does not bar certification." No verdict, no byte moves.

### diagrams-01 — Appendix H reader checklist → CONFIRMED, editorial

Verified against §2.3's actual text and §21.6's closing paragraph
("`[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the
file conforming all the same"). Downgrade rests on Appendix H's own
header: "each entry's authority is the requirement or section cited,
never this summary," and on [R-CNT-15]'s unqualified reject-file, which
no non-normative summary displaces. Real implementer cost (a missed
rejection path found late), no fork.

### diagrams-02 — [R-CNT-27] ordering → PARTIAL, editorial

The ordering gap in §5.1/§6.2 is real; §21.2's preamble is the only
place that orders F5 behind the version gate. But both consequences the
reporter names are foreclosed. The diagnostic class is a SHOULD
([R-CNT-07]), outside the register by [R-CNF-12]. The verifier verdict
is fixed by [R-CNF-11] in terms: *cannot establish* is available "where
some requirement is one it is unable to check on a capability or
resource ground, **as when the file names a format major version it
does not implement**". So a verifier does not report nonconforming
here. And under major 1 both orderings reject-file. Inert today; the
whole case is a hypothetical future major.

### diagrams-03 — §4.7's folding promise → CONFIRMED, editorial

Verified: §7.2's table gives ranges in the Field cell for `type` and
`flags` only. The promise sits in a *Note*, non-normative under
[R-CNF-01]: "All text in this document is normative except: §1 …; any
text labeled *Note*, *Example*, or *Rationale*". The three ranges are
stated normatively at [R-ENC-03], [R-CNT-12], [R-CNT-13], [R-CNT-18]
and cited from §19.1/§19.3. Presentation only.

### diagrams-04 — §18.2's "1 or 2" cell → PARTIAL, editorial

The cell reads "1 or 2; **see below**" — an explicit deferral, not a
statement of the conforming set. The prose directly under it gives the
full four-way partition, and §21.6 fixes the experimental case:
"Ignored (ignore-record); the file is conforming". So the cell does not
assert the strict reading and no implementation can defend rejecting
0x85 from it. The genuine residue is that this is the one place the
"Valid values" column defers rather than states — worth tightening.

### diagrams-05 — §21.6's sentinel row → CONFIRMED, editorial

Both divergences verified against [R-TYP-08] ("inside the layer's
extents", "for each channel the tile carries") and §19.4 step 4.
Downgrade rests on §21.1's own precedence device, in terms: "§21.6's
entries restate their governing rules on the same terms a row does, and
where such an entry and the rule it cites diverge, **the rule governs**
there too" — plus [R-GEO-04]'s "a reader MUST NOT return padding
positions as samples". The row cannot license a return forbidden
elsewhere.

### register-01 — §21.1's unidentified rules → PARTIAL, editorial

Mechanically confirmed: no terminal identifier in §21.1–§21.6. But
§2.1's Note states what a *requirement* is in this document: "every
requirement names the actor it binds (writer, reader, updater,
verifier, or file)". §21.1's rules bind no actor — they are
interpretive rules about the register's relation to the requirements.
So §2.2's "Normative requirements carry identifiers" does not
obviously reach them, and reading (b) — "identifier-bearing text is the
normative surface" — is refuted by [R-CNF-01], which makes all
unlabelled text normative regardless of identifiers. Reader and writer
behaviour is unmoved either way ([R-CNF-04], [R-CNF-11], [R-RDR-02]
carry every obligation). The [R-VEC-02] concern is thin: the manifest
records "the §21 register **row** it exercises together with **that
row's** governing requirement identifier", and every row has one.

### register-02 — §21.6's [R-WRT-08] citation → CONFIRMED, editorial

Verified: [R-WRT-08] reads "An updater MUST NOT re-encode a record
whose type it does not implement, and MUST NOT modify one except by
relocating its extent and re-pointing its slot under §20.5" — nothing
about preserve-or-drop. §20.4's table carries the rule and carries no
identifier. Downgrade rests on [R-CNF-06]: an updater "MUST honor the
preservation obligations of §20.4" — reached by section, so an updater
built from §20 gets it right. §21.6 constrains no accept/reject verdict.

### register-03 — §20.5's "(F36, L25, R1)" → CONFIRMED, editorial

The six omitted reserved-range rows (L31, L33, L34, L36, L43, L45)
exist and say what is needed; I spot-checked L31, L33, L34, L36, L43,
L45 in §21.3. Downgrade rests on the fact that the underlying claim
verifies for every space: a compactor meeting a reserved-range codec,
type, layout, linearization, filter or index_encoding fails §19.3's
layer validation, which [R-WRT-09] obliges, and §20.5's "A compactor
MUST refuse to compact when any check `[R-WRT-09]` obliges fails"
bites. Same refusals, listed or not.

### register-04 — §21.1's "— F27 and L48" → PARTIAL, register-bookkeeping

Reading (B) is available only to someone who does not look the rows up.
The semicolon closes the [R-CNT-22] conjunct, and the row texts settle
it: F27/L48 are [R-MTA-05]'s unsorted-document rows, F28/L49 are
[R-CNT-22]'s stored-flag rows — I checked all four cells. No behaviour
moves; the cost is a mis-attributed corpus entry under [R-VEC-02].

### register-05 — R7/R8 overlap on bare NaN → CONFIRMED, register-bookkeeping

Verified. R8 is not a *strict* specialization of R7 (R8 also covers
`1e400`, which is well-formed JSON), so §21.1's specialization device —
"F1 of F6 and of F8, F35 of F36, L24 of L25" — does not reach the pair
and could not without redrawing one row. Downgrade: both rows carry
outcome ignore-record, detector reader, detection at extent use, so no
reader's treatment of any byte differs and the file is nonconforming
either way. Cost is confined to corpus attribution, where [R-VEC-02]'s
fallback already applies ("the entry records every row the file
exercises and says which it was built for").

### register-06 — 2^62 ceilings derived or chosen → PARTIAL, editorial

Downgrade rests on L39 and L29 themselves, which register "A above
2^62" and "A_slab above 2^62" as instances with detector *reader* and
detection at layer access, and on [R-SLB-01]: "Writers MUST NOT emit
any other nonzero value; a reader MUST treat one as a validity error at
layer scope." A = 2^63 is rejected under either reading. I also checked
the corpus corollary the reporter raises: under **both** readings the
total stays 273, because §21.1 records a file against the narrower row
and L39/L29 are narrower than L1. Nothing open for an implementer; the
"Two do not" accounting is a prose claim about provenance.

### adversary-02 — §16.1's "every stored tile" → CONFIRMED, register-bookkeeping

The document decides it, against §16.1's bare wording. [R-IDX-03]:
"Such an entry contributes no stored extent to the *verifier* rows,
which bind over well-formed entries' extents only" — and §15.3's table
lists "alignment or slab invariant violated (§16)" as one of exactly
three *verifier* rows. So L40 does not fire on a structurally-bad
entry. §16.2 says it in the open for slabs and L41's Condition cell
carries it; §16.1 and L40's cell do not. Downgrade: the file is
nonconforming either way (T8), no reader obligation moves at all —
§16.1: "readers are not obligated to — offsets are always explicit, so
alignment is reader-invisible" — and the cost is confined to which
scope a verifier records and to the L40 vector's [R-VEC-04] sibling
pair.

### writer-02 — Appendix G's unpinned tiling and layout → PARTIAL, editorial

Verified quotes: §11.3's Note — "Tile extents are a writer's choice,
and this specification imposes none"; §14.4's Note — "A single-channel
bool layer does not — ⌈P/8⌉ packed bytes planar versus P bytes
interleaved — and both forms are valid". The asymmetry with item 5's
justification is real. Downgrade rests on Appendix G's own header
"(non-normative)" and its second sentence: "It adds no requirement to
any actor: a writer ignoring it is fully conforming." Both tilings and
both layouts are already conforming and already licensed by
[R-CNF-05]. There is also a live counter-reading the reporter does not
price: the profile speaks of "two conforming writers given the **same
input**", and a layer's declared geometry, layout and channel schema
are plausibly part of that input rather than writer freedom — which is
why the maintainer's repair may be a preamble sentence rather than two
new items.

### writer-03 — §21.5's signpost → CONFIRMED, editorial

Verified both halves: §21.5's second exception ("except where a reader
or verifier declines the decode on the size bound or on the frame's
declared window") and §21.5's closing "§21.6 lists the ignore-record
conditions that are not violations"; §21.6's table carries two
ignore-record non-violation rows and its closing prose names two
capability refusals, none of them the bound-decline. Downgrade rests on
[R-ERR-04]'s MAY and [R-MTA-09]'s own text, which state the decline
completely where they stand: "the file exceeds a §21.9 guarantee and so
remains conforming while the reader MAY decline it (`[R-ERR-04]`)". The
diagnostic class an implementer picks (resource limit vs corruption) is
already fixed by [R-ERR-04]'s last sentence.

### quiz-01 — "the bound above" → CONFIRMED, editorial

Real local under-determination; two bounds precede in consecutive
sentences. Downgrade rests on [R-CNF-11], which reaches every reading:
*cannot establish* is for "some requirement … it is unable to check on
a capability or resource ground", and both declines are that. §21.5's
preamble names the pair explicitly. Same verdict under all three
readings.

### quiz-02 — §2.3's over-wide MU = 1 carve-out → CONFIRMED, editorial

The clause does literally reach sub-records. Downgrade rests on
[R-CNT-18]: "an unknown sub-record type with MU = 1 is reject-layer,
and where the file is otherwise conforming a reader **MUST NOT reject
the file for it**", and on §21.6's closing prose: "The qualifier is
load-bearing — the same type as a layer sub-record is reject-layer and
never a ground to refuse the file (`[R-CNT-18]`), so only the top-level
case is a file a reader refuses." A withdrawn duty cannot license the
act a MUST NOT forbids. Real implementer trap (a checklist reader loses
every other layer in the file), no fork.

### quiz-03 — keywordless "is ignore-record" vs [R-ERR-04]'s MAY → PARTIAL, editorial

The reporter says "The only text putting the two together is a Note."
That is not quite right, and it is the premise the downgrade turns on:
[R-MTA-09] itself, in normative text one sentence earlier, invokes
[R-ERR-04]'s permission for the window case — "the file exceeds a
§21.9 guarantee and so remains conforming while the reader MAY decline
it (`[R-ERR-04]`)" — and [R-ERR-04] is normative and independently
licenses the whole-file decline. So the reconciliation does not rest on
the Note alone, and the resulting divergence is *licensed*, not
ambiguous: [R-ERR-04] says in terms that a file exceeding a guarantee
"remains conforming, and a reader MAY decline it". Two conforming
readers serving one conforming file differently, under an explicit MAY,
is not a fork in the emittable or acceptable set. The residue worth
fixing is that §18.2 states the outcome in a keywordless declarative
whose plain reading forbids what [R-ERR-04] permits.

## Count

21 input ids, 21 groups, each id in exactly one group. Byte-level: 2
(writer-01, adversary-01).
