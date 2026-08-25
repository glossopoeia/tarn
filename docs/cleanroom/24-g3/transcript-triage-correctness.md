# Round 24 triage — correctness lens — working transcript

## What I read

`spec/tarn.md` only, in these ranges (all line numbers from the 4445-line file):
section index (grep of headings); §2.3–§2.5 (134–280); §4.2–§4.3 (382–430);
§4.7 (519–556); §5.1 (557–618); §5.2 (618–695); §6.1–§6.3 (693–830);
§7.2 (899–975); §7.4 (1000–1115); §8.1–§8.2 (1113–1156); §9.1–§9.3 (1156–1230);
§9.7 (1321–1372); §11.4 (1540–1590); §14.3–§14.5 (1887–1985); §15.1 head (1987–2000);
§17.3–§17.4 (2357–2400); §18.1–§18.4 (2417–2630); §20.1–§20.2 (2900–2934);
§20.3 (2934–3142); §20.5 (3192–3320); §21.1–§21.7 (3319–3705); §22.3 (3833–3880);
§23.1–§23.2 (3908–3960); Appendix H (4374–4445).

I read **no** walk transcript and **no** `transcript-triage-*.md`. I ran `ls` on the
round24 directory once, before reading the instruction not to — the listing showed
nine file names including three `transcript-triage-*` names I did not open. I did
not open, grep, or otherwise read any of them.

Mechanical checks I ran myself (python, on the spec):
- register row/instance count by section: F 36/58, L 49/116, T 26/55, R 10/48 →
  **121 rows, 277 instances**, matching §21.8. R7 contributes 6 of those.
- grep: `[R-LIF-02]`, `barrier`, `durabl` do **not** occur anywhere in §20.5
  (lines 3192–3316). `[R-LIF-02]` does not occur anywhere in §21.7 (3632–3705).

## Grouping

G1  reader-01 + quiz-04   §21.7's [R-GEO-06] account and the disk-ordinal half
G2  reader-02             §20.5 version_minor SHOULD antecedent
G3  reader-03 + adversary-02  [R-CNF-03] missing "top-level"
G4  reader-04 + writer-03 + quiz-02 + diagrams-01 + register-03
                          §21.7's list of unwitnessed obligations is incomplete
G5  writer-01             §20.5 never binds a compactor to [R-LIF-02]
G6  writer-02 + quiz-01   index-region regeneration trigger
G7  writer-04             §23.1's two ways omit unstoring
G8  writer-05             R8's instance collapse
G9  verifier-01           §5.2's partial-total exemption scope
G10 verifier-02           verifier verdict for an experimental MU=1 sub-record
G11 verifier-03           no reporting duty for an unassigned-type extent
G12 diagrams-02           Appendix H's verifier checklist
G13 diagrams-03           §21.6's trailer-mimic row justification
G14 diagrams-04           §4.7's Note omits Size
G15 register-01           §21.2's "four rows do reach it"
G16 register-02           "exactly as a mis-strided filter is"
G17 register-04           R7's Condition cell drops the BOM limb
G18 register-05           F31's "1-15" vs L16's "< 16"
G19 adversary-01          §20.3 step 4: (A)'s carve-out vs (B)'s shrink clause
G20 quiz-03               §21.2's sense of "geometry"

27 ids, each in exactly one group. Counted twice: 2+1+2+5+1+2+1+1+1+1+1+1+1+1+1+1+1+1+1+1 = 27.

## The two I graded byte-level

### G19 (adversary-01)

Verified the construction arithmetic myself. d=1, x: E=6, T=4 → G=⌈6/4⌉=2, P=T=4,
one interleaved uint8 channel → decoded size P·Q = 4. Tile 1 covers x∈[4,8);
x=4,5 real, x=6,7 padding. Shrink E 6→5: G=⌈5/4⌉=2 unchanged, entry_count unchanged,
P unchanged, decoded size unchanged, sample byte offsets unchanged, codec/filter
unchanged. Only x=5 goes real→padding, and its stored byte already holds fill 0x00.
T4 passes; the file is conforming under either reading.

I tested the reporter's load-bearing premise — that (A)'s carve-out example ("a new
padding position whose stored byte already holds the fill") has the shrink as its only
referent for a prior-generation stored tile — rather than inheriting it:
- growing E converts padding→real in existing tiles and creates *new* tiles (not
  stored in the superseded generation), so it never adds padding to a prior-stored tile.
  Checked in 1-D (E 6→9, T 4) and 2-D (E (6,8)→(9,8), T (4,4)).
- changing any T changes P and so the decoded size — barred outright.
- changing rank, channel count, or channel order changes P·Q or sample offsets — barred.
- changing fill alters the *content* at existing padding positions, not the *set*;
  §20.3's shape (c) treats it separately.
- linearization has one legal value.
The premise holds. So (A) and (B) collide head-on, and the collision is exactly the
fill-valued case: where the newly-padding byte does **not** hold fill, (A) and (B)
agree (T4 would fire and the tile becomes nonconforming).

I then looked for a sentence that decides it against the reporter, since a downgrade
needs one. The candidate is the shrink paragraph's own test sentence:

> An extent MAY also **shrink**, and the bar above is the whole of the test, **in the
> bar's own tense**: a shrink is permitted exactly where it alters nothing §14 fixes
> for any tile the layer stores in the generation this commit supersedes.

This does **not** decide it, and reading it carefully is what changed my mind. Before
the shrink, §14 fixes nothing about x=5's byte (a real position may hold any value);
after, §14.5 fixes it to the fill. So on the plain words the shrink *does* alter what
§14 fixes, and the test sentence reads *against* permission — while (A), two paragraphs
up, names precisely this case as "not what this bars". The only text that resolves the
test sentence is (A), and (B) then contradicts (A). I could not produce a quotation
that decides it, so I do not downgrade.

Emit-side fork: appender P (reading A) emits the 448-byte generation-2 file; appender Q
(reading B) refuses and must do a whole-file rewrite under a fresh file_id. I checked
that no other conforming writer produces that exact sequence: [R-LIF-02]'s creation
path fixes generation 1 ("with generation 1"), and §20.5 fixes a compactor at
generation 1 under a fresh file_id — so only an appender could, and only via this
shrink. Byte-level: YES, on the emit half only. The accept/reject half does not fork
(every verifier certifies the 448-byte file either way), and I say so rather than
claiming both halves.

### G5 (writer-01)

Verified by grep: §20.5 contains no `[R-LIF-02]`, no "barrier", no "durabl".
[R-WRT-01] binds a compactor to "every writer requirement for the bytes they produce"
plus §20.4. §20.2's [R-WRT-02] binds "a creator", a distinct tier under §20.1.

The pad half is the byte half. [R-CNT-05] states the bound's whole source:

> bounds their number **only through step 5 of the commit protocol**, which pads to the
> next 64-byte boundary (`[R-LIF-02]`) — a longer gap is conforming, and no conforming
> **commit** produces one.

So if a compactor performs neither a commit nor a creation, nothing bounds its
pre-trailer pad; if it does, the pad is exactly (−dir_end) mod 64. §2.3 confirms a
longer gap is a *writer* obligation whose violation is expressly not a file-conformance
violation, and that such obligations "bind the actor in the same way" — so the two
readings differ in which files a conforming *compactor* may emit while both files are
conforming files. That is the byte-level test as stated.

The strongest text for reading A, which I state so it can be attacked: §6.3's
[R-CNT-08] — "A compactor, though its output is a new file, carries the input's unknown
ignore-lane bits into its output trailer rather than writing flags = 0" — displaces one
*creation* rule for the compactor, which presupposes the compactor creates a file; and
[R-LIF-02]'s creation paragraph is addressed to "the writer", not to §20.1's creator
tier: "On creation there is no prior trailer: the writer first emits the front signature
block … then performs steps 2–6, writing beginning at offset 16, with generation 1."
§20.5 also sends the compactor to "§9.3's randomness advice", which §9.3 addresses to
"the creating writer". Three indirect hooks, no statement. A is clearly the better
reading; B is reachable by an implementer who reads §20.5 as the exhaustive statement
of a compactor's obligations that it is written to be. Since B is reachable and forks
emitted bytes, I flag it rather than downgrade. The repair is one clause and costs
nothing, which is the right trade at this gate.

## Downgrades, each with the sentence that decides it

**G1** — §21.7's sentence is premised on "a structurally valid tile", which excludes
reader-01's wrong-length planar plane; that premise partly insulates it, which is why
the group is CONFIRMED on the disk-ordinal complaint and not on reader-01's reading (b).
Not byte-level: §21.1 — "neither this completeness clause nor the instance arithmetic
below reaches §21.6's defined non-violations, §21.7's account of what no check detects,
or §21.9's limits" — so §21.7 carries no normative completeness, and T3/T14/T4/L41 are
register rows with fixed outcomes either way. I confirmed the disk-ordinal witness route
is real: T3's and T14's instance cells both enumerate "planar numeric P·Bᶜ", so a reader
derives the expected decoded size per channel block, and swapping two planes of channels
with unequal element sizes yields a length mismatch with no content byte inspected.

**G2** — reader-02's reading (c) is dismissed on a ground that does not hold. [R-MTA-02]
says "A reader MUST NOT let any part of a user-metadata document affect how a byte is
located, decoded, or returned" — choosing the output's version_minor is none of those, so
[R-MTA-02] does not quarantine the document from being read for this purpose, and
[R-WRT-09] states a verification floor ("MUST verify each link of the chain"), not a
ceiling on inspection. §20.5's "its verification depth is [R-WRT-09]'s and reaches no
decoded content" is a statement about verification depth, not a prohibition. And
[R-CNF-12] closes the fork outright: "Deviation from a SHOULD is not a violation for this
purpose". PARTIAL, editorial.

**G3** — [R-CNT-18] decides the reader's duty: "an unknown sub-record type with MU = 1 is
reject-layer, and where the file is otherwise conforming **a reader MUST NOT reject the
file for it**". A reader refusing the whole file is nonconforming, so no accept/reject
verdict forks. The defect is real and is at §2.3, whose clause reads "carrying no record
of a type it does not implement with MUST_UNDERSTAND = 1" with no scope qualifier, while
§21.6 says "The qualifier is load-bearing". One-word repair.

**G4** — decided by §21.1: "The subsections after §21.5 are not part of the register and
carry no rows: neither this completeness clause nor the instance arithmetic below reaches
… §21.7's account of what no check detects". So the omissions breach no stated norm. I did
verify the omissions are factual: `[R-LIF-02]` occurs nowhere in §21.7, and register-03's
construction is sound — a generation n+1 that writes only a pad and a trailer pointed at
generation n's directory leaves gen n's pad/trailer as slack ("everything an earlier
commit superseded"), F7's instances are structures only ("stored-tile extents; tile-index
regions; record extents; sub-record extents"), and [R-CNT-05] says "a longer gap is
conforming". Conforming file, unperformed step 3, no witness.

**G6** — decided by §20.5's own opening: "Given a conforming input the output is a
conforming file." Under the literal trigger the output's entries address the input's tile
offsets, which fails T1 at minimum (a register row, hence a file-conformance violation),
so [R-CNF-05] bars a conforming compactor from emitting it. quiz-01's citation of
[R-MDL-02] — "The output's reference arrays MUST equal the live generation's bit for bit"
— points the same way. The trigger sentence is genuinely keyed on the region being
relocated, so the group is CONFIRMED; it just cannot fork bytes.

**G7** — decided by the rule's own quantifier: "Writers and the tools built on them MUST
NOT represent **any commit that makes sample data unreachable** as erasure of it." The
enumeration is incomplete — §20.3 step 4 lists three dispositions ("tiles this commit
stores or supersedes … tiles that become unstored written as the sentinel … entries new
to this generation") and §23.2 points back at §23.1 for a case §23.1 does not list — but
the obligation reaches the omitted case anyway.

**G8** — decided by [R-MTA-04]: "A document is unreadable if it contains a number whose
binary64 interpretation is not finite … or any of the bare tokens `NaN`, `Infinity`, or
`-Infinity`". All four forms are ignore-record either way. R8's "alike" is exactly
§21.1's licensed T24-style collapse, so the row is within the letter; the cost is corpus
coverage under [R-ERR-02], not conformance.

**G9** — decided by [R-CNT-21]'s own antecedent: "**a verifier that reaches a live state**
MUST report the total number of slack bytes". A verifier that rejects at F5 or F6 never
reaches a live state, so the duty never fires and the partial-total limb — which modifies
that duty — has nothing to modify. Reading (2) requires ignoring that clause. PARTIAL:
the mid-sentence gloss does name §6.2 alone, which is a real if minor imprecision.

**G10** — REFUTED. §2.3's verifier bullet states the verdict the reporter says is
unstated: "*cannot establish* — the last where some requirement is one it is unable to
check on a capability or resource ground, as when the file names a format major version
it does not implement, **when a record carries MUST_UNDERSTAND = 1 with a type it does
not implement (§21.6)**". That ground is unqualified as to scope and correctly so — a
verifier cannot check an unimplemented type's requirements at either scope. §21.6's
carve-out is about *refusing the file*, not about the verdict label, and the two are
consistent: reader accepts the file, rejects the layer; verifier reports cannot establish.

**G11** — decided by §8.1's map row itself ("none — the bytes are opaque (§7.2)") and
§21.6's row making an experimental-range MU = 0 record conforming: no reporting duty is
stated, so none exists, and the verifier's verdict is *conforming* either way. Also
correcting the reporter: §22.3's "equally invisible" compares the unassigned-type extent
to **slack**, not to the user-metadata extent — "The extent of a record of a type this
specification has not assigned is covered by no checksum either (§8.1), so corruption
inside it is equally invisible". The asymmetry with [R-MTA-10] is real; the gloss is not.

**G12** — PARTIAL. Appendix H's subject is "the live-state coverage partition and the
slack total (**§9.7**)", and §9.7's walk is defined to begin at a live trailer: "A
verifier checking [R-CNT-02]'s partition walks the live state only. From the live trailer
it reads the live directory…". A file rejected at its trailer magic has no §9.7 walk at
all, so the entry's subject does not arise there and it does not "demand" a partial total.
Add that the appendix disclaims itself — "each entry's authority is the requirement or
section cited, never this summary" — and the CONTRADICTION grading overstates. The
three-state distinction is worth restoring in the entry all the same.

**G13** — decided by §21.1: "§21.6's entries restate their governing rules on the same
terms a row does, and where such an entry and the rule it cites diverge, the rule governs
there too." [R-LIF-06] is the right rule and Inert is the right verdict; only the first
justification clause ("nothing enumerates slack") belongs to the slack case rather than
to the payload case the row states, which §22.3 keeps apart.

**G14** — decided by [R-ENC-06]: "No field's width is ever a writer choice: every field's
width is fixed by this specification". §7.4's Type column carries u8/u16/u64 for every
fixed field and §4.2 fixes those widths, so no width can be read two ways. I checked the
other five layout tables against §4.7's contract: §6.2, §15.1 and §18.2 give six columns;
§6.1 gives Offset/Size/Value/Class, which the Note covers; §7.2 gives five, which the Note
covers; §7.4 gives Field/Type/Constraint — omitting offset, **size**, and class, where the
Note names two. Confirmed.

**G15** — not byte-level: both readings leave every reader at reject-file (the version
gate, or F6/F8/F14), and neither verifier certifies. What is genuinely open is which of
§2.3's three labels a verifier prints, and the document pulls both ways: §2.3 says a
foreign-major file "is neither conforming nor nonconforming under it", while also saying
"An established violation takes priority: a verifier that has established any violation
reports *nonconforming*" — and [R-CNT-24] does state a requirement about that file's bytes
("the front signature block (§6.1) is constant" in every major). I lean reading (a) with
the reporter, but this needs a maintainer's decision, not an edit.

**G16** — the substance is already decided by T26's own cell — "the check that detects it
is T2's or T4's" — and by §21.7's own later sentence "the check that detects it is T2's or
T4's, exactly as T26 has it". I verified the reporter's shuffle argument independently:
§17.3 places byte i of group j at offset i·n + j with n = L/s; setting i = s−1, j = n−1
gives (s−1)n + n−1 = sn − 1 = L−1, whose source offset is (n−1)s + (s−1) = L−1. The last
byte is a fixed point for **every** stride dividing L, so both the writer's wrong-stride
shuffle and the reader's correct-stride inverse fix it, and a packed plane's pad bits —
which live in that final byte — are unchanged. T5 can never witness a wrong stride. The
defect is the loose "exactly as a mis-strided filter is" sitting directly after the
three-row list "T2, T4 or T5".

**G17** — decided by [R-MTA-04]: "the encoding carries no byte-order mark: a leading
U+FEFF makes the document unreadable", plus §21.1's "where a row and the rule it cites
diverge, the rule governs". I checked the arithmetic claim myself: the register totals
121/277 come out exactly, and R7 contributes 6 — but they are computed from the
**Instances** cell, which §21.1 says is where the mechanical count lives ("Instances
within a cell are separated by semicolons … the count is therefore mechanical once the
cell is written"). So no counting defect exists; the defect is the Condition cell's
incomplete restatement of [R-MTA-04]'s first restriction.

**G18** — decided by §21.1's tie-break plus [R-CNT-13]'s "an extent_offset < 16". F31's
"in 1-15" is a divergence with no normative force; L16 renders the same clause as "< 16".
Same outcome, same detector, same detection point either way; only corpus attribution for
the slot (0, nonzero) moves.

**G20** — decided by [R-CNT-06]: "A reader MUST validate, in order: the trailer magic; the
trailer CRC; the version gate (§6.3) … and then, those gates passed, MUST validate all of
the following". The ordering fixes which checks a foreign-major file meets, independently
of the paragraph. Verified the reporter's terminology survey by grep: every other
occurrence of "geometry" in the file (lines 91, 1041, 1440, 1467, 1508, 1919, 2804, 2988,
3024, 3030, 3031, 3127, 3480, 3491, 3813, 3934, 4206) is a layer's geometry; line 3401 is
the only file-byte-geometry use, and §21.2's table contains no layer-geometry row, so the
layer sense would make the carve-out vacuous.
