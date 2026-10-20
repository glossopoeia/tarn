# Writer/updater fidelity walk — edition B — transcript (writer-b)

## Disclosure

- **Access.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
  in full, via paginated reads (it is ~291 KB / 4810 lines, over the single-read
  size cap, so I read it in five sequential chunks: lines 1–1200, 1201–2400,
  2401–3000, 3001–3600, 3601–3930, covering Parts 0 through III up to §21.7). I
  did not open any other file. I ran `grep`/local `python3 -I` arithmetic only;
  no other file reads.
- **Unbidden context.** Before I began, my context already contained: a
  `CLAUDE.md` project-instruction pointer to `AGENTS.md`; a user memory file
  (`MEMORY.md`) listing many TARN-process notes (harness spec path, lineage
  gate word list, preflight checks, repair prose vs rules, harness vs charter,
  etc.); a git-status block naming the current branch (`readable`), recent
  commit subjects, and the git user; an attribution/co-authorship instruction
  block for commits and PRs; and tool/skill listings. None of this is part of
  the specification and none of it is evidence about the specification; I have
  not treated any of it as such, and I am not repeating its contents further
  than naming that it appeared.
- **Relayed user request.** A harness message labelled "user request" and
  reading simply "Go" was prepended above the computed task. Per the brief,
  this is the launcher's message to the orchestrator, already carried out,
  not a task for me, and it does not widen the access rule. Noted and set
  aside.
- **Paths.** The file was exactly where the brief said:
  `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`. No
  discrepancy to report.
- **Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/walk-writer-b/`
  was empty (only `.` and `..`) when I started — no previous attempt's files
  were present. I created one file there, `arithmetic.py`, holding the index-
  region-size and smallest-file arithmetic I verified by local computation
  (no file reads in that script; run under `python3 -I`). Its output matched
  the document's own worked examples (644-byte index region for 32 entries;
  16 segments / 16,960-entry final segment / 64-byte CRC array for
  1,000,000 entries, matching §15.4's own example).
- I did not list or read the output directory `fidelity-5/out/` beyond
  writing this one file to it.

## Method

I read Parts 0–III of the document (Introduction through §21.7, stopping
after confirming the error-register rows I needed in §21.2–21.6). The
charter's subject matter — creation layout, the append procedure, slack,
preservation/drop rules, rewriting, torn-write recovery — lives almost
entirely in §5, §6, §9, §15, §16, §20, and the register in §21.2–21.5, all of
which I read in full. I did not read §22–24 or the appendices; nothing in the
probes or the charter turned on security/privacy considerations or the
non-normative appendices, and the brief asks me to disclose a zero rather than
assert completeness I did not check. Before resting any conclusion on a grep
returning zero, I ran a control search for a nearby phrase I expected present;
in practice I did not end up needing line-oriented grep against wrapped prose,
since the Read tool returns unwrapped line-numbered text and I worked from
that directly, but I did use `grep`/`rg` to jump to section headers and to the
T4/T5 register rows to confirm exact wording before quoting them.

---

## The walk

### 1. Creation byte layout — smallest conforming file

`[R-CNT-27]`: "No conforming file is shorter than 128 bytes: the front
signature block, a directory of at least 4 bytes at an offset of at least 16,
and the 64-byte trailer at a 64-aligned offset cannot be satisfied in fewer."

The document's own worked example (§5.1) gives the layout directly:

> "The smallest conforming file is exactly 128 bytes: front block [0, 16); an
> empty directory — zero records, so 4 bytes holding the CRC-32C of zero
> bytes, `0x00000000` — at [16, 20); 44 bytes of slack, zeroed by advice;
> trailer at [64, 128). It contains no layers (a valid, empty file)."

Regions with offsets (half-open, bytes):

| Region | Offsets [start, end) | Size |
|---|---|---|
| Front signature block | [0, 16) | 16 |
| Directory region (record sequence + CRC) | [16, 20) | 4 (0 records + 4-byte CRC) |
| Slack (pre-trailer pad) | [20, 64) | 44 |
| Trailer | [64, 128) | 64 |

Trailer field values (§6.2's layout table, at F = 128):

- `trailer magic` = `8A 4E 52 41 54 0D 0A 1A`
- `version_major` = 1 (this is the only format major this text defines;
  §6.3: "a reader MUST reject-file when version_major is 0 ... or is a major
  it does not implement")
- `version_minor` = 0 — §6.3: "A writer SHOULD emit the lowest version_minor
  that defines every feature present in the file (for a file expressible
  under this text, version_minor is 0)." This field is descriptive
  (`[R-ENC-16]`), so this is the SHOULD-recommended value, not a hard
  requirement; a creator writing a higher minor that defines no feature
  actually present would still be conforming but is not what the document
  recommends.
- `flags` = 0 (bits 0–31 all zero) — §20.1/`[R-WRT-01]`: "As a creator it
  undertakes nothing toward its input, whatever it read: §20.2 binds it, it
  writes flags = 0." §6.3: "This specification's text defines no flag bits,
  so a writer creating a file under this text MUST write flags = 0."
- `dir_offset` = 16 (≥ 16 per `[R-CNT-06]`; here the minimum)
- `dir_length` = 4 (≥ 4 per `[R-CNT-06]`; here the minimum)
- `committed_file_length` = 128 (= F, multiple of 64)
- `file_id` ≠ 0 — a writer's choice, not a fixed value. §9.3: "the file_id is
  nonzero, and the creating writer SHOULD draw it from a cryptographically
  random source." The document does not fix what this value is, only that it
  is nonzero; I am not inventing a specific number.
- `reserved` [48, 60) = 12 zero bytes (`[R-CNT-06]`: "reserved bytes all
  zero")
- `trailer CRC` [60, 64) = CRC-32C over trailer bytes [0, 60) — a computed
  value that depends on the chosen `file_id`, so I report the formula rather
  than a number, consistent with the document treating `file_id` as the
  writer's free choice.

The directory region's own content: 0 records, 4-byte CRC = `0x00000000`
— directly from the document's check vector, §4.5: "The CRC-32C of zero
bytes is `0x00000000`."

---

### 2. Append — superseding one tile of a 32-tile interleaved layer

**W2** (below) gives this in full; summarizing the byte-layout walk here.
§20.3's own worked example states it exactly:

> "Superseding one 100,000-byte stored tile of a 32-tile interleaved layer
> appends: the new payload (100,000 bytes), the layer's full new index
> region (32 · 20 + 4 = 644 bytes: one entry re-pointed, 31
> byte-identical), the new directory (every record byte-identical except the
> modified layer's), the pad, and the 64-byte trailer. The prior index region
> and the superseded payload become slack, reclaimable only by a rewrite
> (§20.5)."

I verified the index-region arithmetic independently (`entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4`, `[R-CNT-17]`): 32 × 20 + 1 × 4 = 644. Confirmed by
script (see disclosure).

---

### 3. Record flags — every combination, and what an updater may do

The record-framing flags (§7.2) are two bits: `MUST_UNDERSTAND` (MU) and
`PRESERVE_ON_EDIT` (PE). `[R-CNT-12]`: "Writers MUST NOT emit the combination
MU = 1 with PE = 0; a reader or updater encountering it MUST treat the record
as PE = 1 (never silently deletable)." The Note immediately after: "The two
flag bits are not orthogonal. `[R-CNT-12]` leaves a record three states, not
four, and they are §20.4's three rows: MU = 1, whose PE bit is read as 1
whatever is stored; MU = 0 with PE = 1; and MU = 0 with PE = 0."

§20.4's table (quoted in full, since the probes turn on its exact wording):

| Governing flags | Updater obligation |
|---|---|
| MU = 1 | Retain byte-identical. The updater MUST NOT modify the scope the record governs. At layer scope an unknown critical record blocks modification of that layer, its drop included, leaving other layers editable (`[R-CNT-18]`). At file scope no commit is available at all: the updater is a reader of the file first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file — the same treatment §6.3 gives an unknown incompat-lane bit. At either scope a rewriter MUST refuse to rewrite the file, on `[R-WRT-06]`'s own ground: such a type can define references this specification does not (§7.2), so its bytes cannot be safely relocated. |
| MU = 0, PE = 1 | Retain byte-identical, extent content unmodified. |
| MU = 0, PE = 0 | Retain byte-identical, or drop it — its extent becoming slack. The licence is the bit's own ... an appender MAY drop the record in any commit it is otherwise free to make — one whose only effect is the drop included — and a rewriter MAY drop it in any rewrite. An updater that drops such a record SHOULD report the loss; unreported, application state disappears with no diagnostic. |

But — and this is load-bearing for which row governs in W11 — which flags
*govern* a given record is not always its *stored* bits:

> "Persistence governs every record type; only the authoritative source of
> the flags differs. For a type §7.3 registers, the registry's fixed flags
> govern rather than the stored ones (`[R-CNT-22]`) ... For a type the
> updater implements that this specification does not register, the
> definition it implements the type from supplies the flags, and the stored
> bits never do (`[R-CNT-22]`, §10.3). For a type the updater does not
> implement, the stored flags are authoritative (§7.3, `[R-CNT-15]`; MU = 1
> with PE = 0 is read as PE = 1, `[R-CNT-12]`). ... Its MU = 1 row reaches
> only a type the updater does not implement, since an updater implements
> both registered types and understands an unregistered type it implements
> from its definition, modifying their records as §20.3 and that definition
> provide; so for an implemented type only the PE bit bites."

### W3. Appender's input carries a top-level record of an unimplemented type, MU = 1

§20.3 step 2 (Open): "A violation the open establishes bars the commits its
outcome bars and no others: reject-file bars every commit" and, from §20.4's
table (MU = 1 row): "At file scope no commit is available at all: the
updater is a reader of the file first (§2.3), and `[R-CNT-15]` makes an
unimplemented top-level MU = 1 record reject-file."

**What the appender may do to the file:** nothing. Because the type is
unimplemented and MU = 1, `[R-CNT-15]` ("A record at file scope whose type
the reader does not implement is governed by its stored MU bit: MU = 1 is
reject-file") fires at open (§19.1 step 4, which every appender performs per
§20.3 step 2), before any commit decision is reached. The appender — a
reader first — must reject the whole file and cannot append to it at all;
there is no partial commit, no commit that merely avoids touching the
record, available to it. (Contrast with an unimplemented layer *sub-record*
with MU = 1, which is reject-*layer*, §20.4's table: "At layer scope an
unknown critical record blocks modification of that layer, its drop
included, leaving other layers editable" — the appender can still commit
against other layers. The probe names a *top-level* record, so the file-wide
bar governs.)

**What a rewriter may do:** also nothing — it must refuse outright.
`[R-WRT-06]`: "A rewriter MUST refuse to rewrite a file carrying any record
whose type it does not implement with MU = 1: such a type can define
references this specification does not (§7.2), so its bytes cannot be
safely relocated." §20.4's table states the same for both scopes: "At
either scope a rewriter MUST refuse to rewrite the file."

### W4. Top-level record, unimplemented type, MU = 0, PE = 0

Governing flags here are the *stored* ones, since the type is unimplemented
(§20.4: "For a type the updater does not implement, the stored flags are
authoritative"). MU = 0, PE = 0 is the table's third row.

**May an appender drop it in a commit whose only effect is the drop?** Yes.
§20.4's table: "Retain byte-identical, or drop it — its extent becoming
slack. The licence is the bit's own ... so an appender MAY drop the record
in any commit it is otherwise free to make — **one whose only effect is the
drop included**" (my emphasis on the exact clause the probe is testing).

**May a rewriter drop it?** Yes — same table row: "a rewriter MAY drop it in
any rewrite."

**Must either report the loss, and under which keyword?** SHOULD, not MUST.
Table: "An updater that drops such a record SHOULD report the loss;
unreported, application state disappears with no diagnostic." This is an
advisory (SHOULD), not a hard MUST obligation; failing to report does not
make the file nonconforming (reporting is a conduct matter, like the commit
barriers of `[R-LIF-02]` steps 4/6, not a byte-level property of the file
itself).

### W9. Dropping a layer whose own record is PE = 0, carrying an MU = 1 sub-record

The layer record itself is registered (type 0x0001) and always governed by
the registry's fixed flags: "the layer record carries PE = 0 and is dropped
under the table's last row" (§20.4). Read alone, that licenses a drop. But a
sub-record of the layer, of a type the updater does not implement, stored
with MU = 1, changes the answer — I searched §20.3 and §20.4 for every
sentence bearing on this:

- §20.4, directly: "A commit MAY therefore drop a layer record, and the drop
  takes the layer whole: a sub-record's flags govern it within a layer the
  updater keeps, so a dropped layer's sub-records and their extents go with
  it whatever their PE bits. **One sub-record blocks the drop, a sub-record
  of a type the updater does not implement with MU = 1, the drop being a
  modification of the scope it governs (the table's first row).**"
- §20.4's MU = 1 table row, quoted above: "At layer scope an unknown
  critical record blocks modification of that layer, its drop included,
  leaving other layers editable."
- §7.2, on sub-record framing generally: "Writers MUST NOT emit the
  combination MU = 1 with PE = 0; a reader or updater encountering it MUST
  treat the record as PE = 1 (never silently deletable)" — consistent with,
  not contradicting, the above: whatever the sub-record's own PE bit says,
  MU = 1 blocks.

**May the commit drop the layer? No.** The layer record's own PE = 0 is
necessary but not sufficient; the presence of one MU = 1 sub-record the
updater does not implement overrides it, because "the drop" of the layer is
itself "a modification of the scope [the sub-record] governs" (the layer),
and an MU = 1 record's governing rule is "the updater MUST NOT modify the
scope the record governs." I found no sentence that disagrees with this:
every passage that speaks to it — the general sub-record quotation above,
the layer-drop paragraph, and the table's MU = 1 row — agrees, and none
license dropping a layer over an unimplemented MU = 1 sub-record's
objection. (Contrast W4's scenario, a *top-level*, not layer-governed,
record: there the layer-scope override has no sub-record to block it.)

### W10. Appender carries forward a top-level MU = 0 / PE = 0 record unmodified, wants to drop it

Both relevant passages, cited exactly, to check agreement:

- §20.3 step 2 (the append procedure): "Against any other structure the
  appender carries forward, it MUST NOT repair the defect, since
  `[R-LIF-01]` freezes the committed prefix, and **MUST NOT drop the record
  save where §20.4 licenses the drop**."
- §20.4 (the preservation table, PE = 0 row): "Retain byte-identical, or
  drop it — its extent becoming slack. ... an appender MAY drop the record
  in any commit it is otherwise free to make — one whose only effect is the
  drop included."

**They agree.** §20.3's "save where §20.4 licenses the drop" is exactly the
carve-out that §20.4's PE = 0 row then grants; there is no tension between a
general "MUST NOT drop" in the append procedure and a specific "MAY drop"
license in the preservation table — the first explicitly defers to the
second. So: yes, the appender may drop it, even in a commit whose only
effect is that drop, and SHOULD report the loss.

### W11. Updater implements an unregistered type whose definition fixes MU = 1, PE = 0

This is where I found the document's answer less settled than W3/W4/W9/W10,
and I want to lay out the tension rather than silently pick a side.

The table's row structure is explicitly derived from `[R-CNT-12]`'s
collapse of MU/PE into three states (not four), per the Note at §7.2: "MU =
1, whose PE bit is read as 1 whatever is stored." Taken alone, that note
reads as unconditional: wherever MU = 1 is the governing bit, PE is read as
1, full stop, which would mean an MU = 1, PE = 0 definition still lands in
the table's first row — "Retain byte-identical... MUST NOT modify the scope
the record governs," no drop — regardless of whether the type is
implemented.

But §20.4's governing-flags paragraph, immediately before the table, says
the opposite about *implemented* types: "For a type the updater implements
that this specification does not register, the definition it implements the
type from supplies the flags, and the stored bits never do ... Its MU = 1
row reaches only a type the updater does not implement ... **so for an
implemented type only the PE bit bites**."

Read literally, that last clause is the sentence that decides which row
governs for W11's case: since the updater *implements* the type, the MU = 1
row (whose consequence is "no drop") does not reach it at all; only the PE
bit — here, PE = 0 — selects the row, which is the PE = 0 row: "Retain
byte-identical, or drop it." Under that reading: the preservation table
obliges either byte-identical retention or a drop (updater's choice, SHOULD
report if dropped), and the updater **MAY** drop a record it does not
modify. The decisive sentence is "so for an implemented type only the PE bit
bites."

I flag this as an ambiguity rather than a settled answer, because the
sentence that decides it (the "only the PE bit bites" clause) sits in
tension with the general three-states Note at §7.2, which frames the MU = 1
→ PE-read-as-1 collapse as unconditional ("whatever is stored") and ties it
directly to the same three table rows §20.4 uses, without itself carving out
an exception for implemented-but-unregistered types. Nothing in either
passage flags the other as an exception explicitly; the two read together
either as (a) the §7.2 Note describing the *general* case and the §20.4
clause being the *implemented-type* exception it doesn't mention, which is
a consistent reading and the one I lean on above, or (b) a genuine
drafting gap where an external definition's MU = 1 / PE = 0 pairing was not
anticipated to collapse the same way a record's own *stored* bits do. I
record this as a finding below (byte-level: it decides whether a conforming
updater may legally drop such a record in an otherwise-unmodifying commit,
i.e., whether the resulting file, with the record present vs. absent, is
produced by a conforming updater either way or only one way).

---

### 4. Slack under each commit shape

§20.3's own figure (quoted in full, since it is the document's own worked
answer) gives three shapes:

**(a) A new layer — nothing existing is rewritten.** Slack is just the old
directory, pad, and trailer (sized by layer *count*, never by any layer's
data): "A's record is carried into dir₂ byte-identically ... The slack is
the old directory, pad and trailer, sized by the file's *layer count*, never
by any layer's data."

**(b) Tiles added to / superseded in an existing layer.** "That layer's
index is re-emitted whole ... The whole region moves because it is addressed
by one extent slot, so a single changed entry costs its whole length ...
Superseded payloads become slack too; retained ones do not move." Slack
here is: the old index region (even if only one entry changed) + every
superseded tile payload + the old directory/pad/trailer.

**(c) A change confined to the directory** (clearing a slab declaration,
renaming a layer, dropping a layer or a PE = 0 record where §20.4 licenses
it). "Only the directory is re-emitted." If a layer is dropped: "becoming
slack" is "a dropped layer's tiles, index region and sub-records' extents."
Otherwise slack is just the old directory/pad/trailer.

In every shape, the pre-trailer pad (`[R-LIF-02]` step 5) and the previous
generation's directory+trailer are slack (§5.2); whether any tile payloads
or index regions join them depends entirely on whether the commit changed a
layer's stored-tile set or index content (shape (b)) versus touching only
the directory (shapes (a)/(c)).

---

### 5. Torn-write recovery at four crash points

All four points share one mechanism, which I want to state before the
per-point detail because it is the document's actual answer to all of them:
`[R-LIF-01]` ("All bytes in [0, F) ... are immutable") plus tail-anchored
discovery (§5.1's closing paragraph: "the structures that change on every
commit are the last ones in the file, so a commit appends and never
rewrites a committed byte") together mean the prior trailer trail_n and
everything it reaches are byte-intact no matter which of steps 1–6
(`[R-LIF-02]`) the crash interrupts, because none of them ever write below
the prior F. The §9.2 worked example makes this explicit:

> "mid-commit │ … │ dirₙ │pad│ trailₙ │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
>                                       ↑ trailₙ intact, but no longer
>                                         at the file's end
> ... Mid-commit the physical tail is not a trailer, so a reader on the
> default path reports the file torn and MUST NOT scan backward
> (`[R-LIF-05]`). What makes that recoverable rather than fatal is that
> trailₙ and everything it reaches are still byte-intact: §9.6's deliberate
> scan finds trailₙ and truncating to it restores the file exactly."

**Point A — crash mid-step 2** (new stored-tile payloads / tile-index
regions partially written, directory not yet started). **Point B — crash
mid/after-step 3, before step 4's barrier** (directory written, not yet
durable — its bytes may or may not have reached stable storage at all).
**Point C — crash after step 4** (directory durable) **but before step 5**
(no pad/trailer bytes written yet). **Point D — crash during/after step 5**
(pad and new trailer bytes written, possibly even completely, but step 6's
barrier never completed, so their durability is not established) — this is
the point **W7** names.

For every one of A–D:

- **What the next reader sees** (default path, §9.5/`[R-LIF-05]`): it
  fetches the final 64 bytes of the *physical* file and finds either no
  valid trailer at all (A, B, C: nothing resembling a complete trailer sits
  at the physical end) or, at D, bytes that may or may not parse as a
  trailer but in neither case can the reader trust them, because the reader
  has no way to distinguish "the barrier simply hadn't returned yet" from
  "these bytes never reached the disk." `[R-LIF-05]`: "a reader that finds
  no valid trailer in the final 64 bytes MUST report the file torn or
  invalid and MUST NOT scan backward." Practically: at A/B/C there is no
  trailer-shaped 64 bytes at the physical end at all (reject against F8,
  the trailer-magic gate), so the outcome is identical across A–C; at D, if
  the new trailer did fully land (bytes complete and would even pass its
  own CRC) a reader on the *default* path still has no way to know this
  reliably post-crash and the specification's model is that only step 6's
  completed barrier entitles trust in it — but note the document does not
  give the *default* reader a special "trust it anyway" rule keyed to
  whether the bytes happen to validate; §9.5/§9.6 draw the line at whether
  this is the reader's *own* open (which never scans) versus a recovery
  tool's deliberate re-verification. I did not find a sentence distinguishing
  "trailer bytes present and self-consistent post-crash" from "trailer
  magic absent" for the *ordinary reader's* behavior; both are simply "no
  valid trailer confirmed by this reader's own process" in the absence of a
  deliberate recovery step, and ordinary-reader behavior is the same reject.
- **Is the file conforming?** Testing the whole current physical byte
  sequence as "the file": no, at every one of A–D, under the ordinary
  reading of `[R-CNT-06]`'s trailer gates (no valid trailer sits at the
  physical end satisfying the magic/CRC/length checks, except in the freak
  case the document separately names, "a payload byte-string that mimics a
  trailer," §21.6, which §9.6's whole-file re-verification is built to
  catch). Testing instead the **prefix** [0, F_old) ∪ {trailₙ at
  [F_old−64, F_old)} = the pre-crash committed state: yes, that byte
  sequence is exactly the prior conforming file, untouched (`[R-LIF-01]`).
- **What the next appender does:** `[R-LIF-04]`/§9.4: "A writer beginning a
  commit against an existing file MUST establish F by validating the
  trailer in the final 64 bytes of the physical file (§6.2). If that
  validation fails, the file is torn: the writer MUST NOT append. Locating
  the last committed state is then the deliberate recovery operation of
  §9.6, never an implicit step of opening for append." So at every one of
  A–D the next appender's own physical-tail check fails (or it declines to
  trust an ostensibly-valid-looking tail from D without the deliberate
  recovery path — the document does not offer an appender a shortcut around
  §9.6 for this case either), it does not append, and it invokes §9.6's
  probe: "Probe backward at 64-aligned offsets o for the trailer magic. On
  a match, require the trailer CRC to verify and committed_file_length = o
  + 64 ... The nearest-to-end candidate that survives the whole-file
  re-verification below is the last committed state, and truncating to it
  recovers the file." That candidate is trailₙ at F_old in every one of
  A–D, since nothing below F_old was ever touched. Then, per §9.4: "Once F
  is established ... a writer whose physical file is longer than F MUST
  either truncate to F before step 1 ... or overwrite from F and truncate
  the physical file to the new committed_file_length no later than step 6."
  The next appender truncates/overwrites from F_old and proceeds with a
  fresh commit exactly as if the interrupted attempt had never begun.

The four points are, in short, operationally indistinguishable in outcome —
same recovered F, same mechanism, same next-appender behavior — which is
precisely what §9.1/§9.2/§9.6 are built to guarantee, and the document says
so explicitly in the Note right after the worked example: "Where barriers
are weaker than assumed, safety degrades from 'torn commits are invisible'
to 'torn commits are detected' — §8's chain still catches every inconsistent
state loudly."

### W5. Ignore-lane bit 20, through three writer tiers

Input trailer flags: bit 20 set (an ignore-lane bit this text does not
define — bits 16–31 are the ignore lane, §6.2/§6.3).

**(a) Appender's commit.** `[R-CNT-08]`: "An updater MUST copy forward
unknown ignore-lane bits of its input file, MUST NOT clear them, and MUST
NOT set any other." §20.3 step 6: "trailer with the same file_id,
committed_file_length equal to the new end ... **unknown ignore-lane flag
bits copied forward and no other set** (`[R-CNT-08]`)." **Output: bit 20
still set, no other ignore-lane bit set, incompat lane still 0.**

**(b) Rewrite.** `[R-WRT-06]`: "The output trailer MUST copy the input's
unknown ignore-lane flag bits forward and set no other, in place of the
flags = 0 §6.3 requires of a file created under this text." **Output: bit
20 still set, no other bit set** — same as the appender, by explicit design
("in place of the flags = 0 ... requires of a file created under this
text" marks this as the rewriter's one deliberate departure from plain
creation).

**(c) A creator that read the input and writes a new file from what it
decoded.** This is the sharpest case, because the document is explicit that
reading the input's bytes confers no obligation toward them once the writer
positions itself as a creator rather than a rewriter: §20.1, `[R-WRT-01]`:
"As a **creator** it undertakes nothing toward its input, **whatever it
read**: §20.2 binds it, it writes flags = 0, and it answers for every byte
of its output (`[R-CNF-05]`), bytes it copied from another file included."
And §6.3: "This specification's text defines no flag bits, so a writer
creating a file under this text MUST write flags = 0." **Output: flags = 0
— bit 20 is cleared.** This is a real, document-stated divergence from (a)
and (b): the same logical content, written by a creator instead of an
updater, loses the unknown ignore-lane bit, and the document does not
treat that as a defect — a creator's only obligation is §20.2's path and
flags = 0, full stop.

### W6. Commit changes only a stored-tile layer's fill value

The channel fill is on the **fixed** list for a layer that stored a tile in
the superseded generation. §20.3 step 4: "Every other declaration is fixed
for as long as the layer stores a tile: the layout, the linearization and
the index encoding, the codec and the filter, the rank and the dimension
order, every tile extent, **every channel's type and fill**, an interleaved
layer's channel list (its names aside), and the position of every planar
channel the new state keeps. A commit MUST NOT change one of these; the
change is a new layer, or a rewrite that re-declares it under a fresh
file_id."

**Is the commit permitted? No.** Changing only the fill value, with the
layer's tiles otherwise untouched, is exactly a change to a fixed
declaration on a layer that stored a tile — barred.

**What operations does the document offer instead?** Two, both named in the
same passage: (1) treat it as "a new layer" — i.e., drop the existing layer
(§20.4's drop licence, `[R-CNT-14]`'s per-name uniqueness freeing the name,
§20.3 step 4: "A dropped layer's name is free to the same commit and to any
later one") and add a new layer, under the same or a different name, with
the new fill; or (2) "a rewrite that re-declares it under a fresh file_id"
— §20.5 names this explicitly as one of exactly three rewrite operations a
rewriter performs: "**re-declaring** a layer that stores a tile in the
input, the rewrite §20.3 step 4 reserves for a change to a fixed
declaration."

**Would the file such a commit leaves be nonconforming?** Here the document
draws a careful distinction I want to preserve rather than collapse. The
bar itself is a *writer-conduct* rule, and violating conduct rules does not
by itself make bytes nonconforming: "This bar binds the commit as an actor:
no file is nonconforming by virtue of its violation, and no register row
records the violation itself, the register enumerating file-conformance
violations (§21.1) and the bar stating no condition a file can exhibit
(§21.7, `[R-ERR-01]`, `[R-CNF-02]`); **a file such a commit leaves can be
nonconforming on its own terms, as the paragraph below sets out**." The
paragraph it points to is the one right after, which names exactly the
observable consequence: changing the fixed declarations reinterprets
"a stored tile's decoded size, a padding position or pad bit, or a boolean
byte the register witnesses (T3, T14, T21, T22, T4, T5, T2)." T4, which I
confirmed by direct quotation (§21.4): "A padding position does not encode,
for each channel it carries, that channel's recorded fill value ...
[Detector: verifier; Governing rule: `[R-SER-05]`]." So: wherever the
layer's tiles include any padding positions for the changed channel (an
edge tile, §11.3), the stored padding bytes — written under the *old* fill
at creation time — no longer match the *new*, re-declared fill value a
verifier reads from the current channel entry, and `[R-SER-05]`/T4 fires:
"a verifier MUST check it, and a violation is a validity error at tile
scope." **That makes the file nonconforming**, detectably, via T4 — but
only in that case. I flag the case where the layer has *no* padding
positions (every dimension's extent divides its tile extent exactly, so no
edge tile ever carries padding) as a genuine gap below (finding
writerb-01): there, nothing in the register detects the changed fill at
all, and the resulting file is conforming despite the writer-conduct bar
having been violated — exactly the "legitimate byte-divergence" the
charter asks me to catalogue, except here it is a *forbidden* change that
is nonetheless byte-invisible rather than a *permitted* one.

### W7. Commit interrupted after directory durable, before trailer durable

Answered in full above under "Torn-write recovery," point C/D. Summary:
next reader on the default path finds no confirmed valid trailer at the
physical end and reports the file torn, `[R-LIF-05]`, never scanning
backward; the file as a whole physical byte sequence is not conforming (no
live trailer is established to anchor `[R-CNT-01]`'s F), while the prefix
up to and including trailₙ is exactly the prior conforming file,
untouched (`[R-LIF-01]`); the next appender's own establish-F step fails
(`[R-LIF-04]`), so it does not append, invokes §9.6's deliberate recovery
scan, which (re-verified) settles on trailₙ at the old F, and then
truncates/overwrites from that F and proceeds — "truncating to it recovers
the file" (§9.6).

### W8. Rewriter carries forward a layer with an "unimplemented sample type"

I want to flag before answering that this probe's premise is foreclosed by
the document for a *conforming* implementation. §12.1, `[R-TYP-01]`: "This
specification defines exactly thirteen sample types, all **core**: a
conforming reader MUST decode every one of them, and none is skippable."
§2.3, `[R-CNF-03]` (conforming reader): "and MUST handle ... every sample
type that §12 designates as core ... There are no subset profiles: software
that declines any of those is not a conforming reader, even if it reads all
other conforming files correctly." §2.3, `[R-CNF-06]` (conforming updater):
"An updater MUST satisfy every writer requirement for the bytes it produces,
and additionally MUST honor the preservation obligations of §20.4" — and
§20.1 makes every rewriter "a reader of every structure it processes"
(`[R-CNF-11]`). So: a tool that does not implement a core sample type is not
a conforming reader to begin with, and therefore not a conforming rewriter
either; the document gives no conformance class for "rewriter missing a
core sample type," because the 13 sample types are a closed, fully-core
list with no skip mechanism (contrast record types, where MU/PE exist
precisely to let an implementation not understand a type). There is no
"experimental" or "reserved" sample-type range an implementer could claim
legitimate non-support for either (§12.2: "values 14 through 19 are
reserved without semantics; values 20 through 0x7FFF are reserved for
future assignment ... values ≥ 0x8000 are the experimental range" — all of
which are *unassigned* types, a different situation than "implements 12 of
13 assigned types").

That said, the document does separately describe what a rewriter does with
content it cannot *decode* for other reasons (a layer using a codec/filter
it does not implement is impossible under the same closed-core argument,
§17.4/`[R-COD-11]`, but a layer using an *assigned* encoding the rewriter
simply declines on resource grounds, or one whose checksums fail, is
on-document), and I answer that version of W8 since it is what the
document actually provides for:

**What it must verify about each stored tile it copies (verbatim, not
re-created):** `[R-WRT-09]`: "A rewriter's verification depth over what it
carries follows reliance (`[R-WRT-03]`): it relies structurally on every
structure it copies, so it MUST verify each link of the chain before
emitting that structure's bytes: the open (§19.1), each retained layer's
record (§19.3) and full index chain (`[R-IDX-04]`), and the checksum §8.1
states over each extent it copies, every stored tile's entry crc among
them." Structural verification only — not a decode: "The duty follows what
the rewriter carries and not where it places it ... What it re-creates it
decodes as a reader first ... What it carries forward is a layer whose
tiles it cannot decode" is exactly the case where it is *not* re-creating,
so it owes the index-chain + entry-crc checks and nothing about content
(§14's decode obligations are the *content* side, owed only when
re-creating or certifying).

**What it does when a checksum fails:** it cannot copy that tile forward as
a valid structure, and §20.5 gives it exactly two disposals for a structure
it cannot safely carry: "`[R-WRT-06]` then leaves it two disposals, since it
can neither reproduce the entry nor invent a replacement: drop the layer,
which §20.4's table licenses and whose loss the rewriter SHOULD report as
that table says, or refuse." (That passage is stated for an entry with no
usable stored extent; a failed entry-crc over an otherwise well-formed
entry is `[R-IDX-03]`'s "the defect lies in the bytes it addresses, not in
the entry, so its extent stands" — still a tile the rewriter cannot
honestly certify or carry forward as valid, and the same two disposals are
what §20.5 offers for anything the rewriter "MUST refuse to rewrite ...
when any check `[R-WRT-09]` obliges fails": "it can neither re-emit the
structure corrected (`[R-WRT-05]`), nor keep it and call the output clean.
Dropping is the one disposal that answers, and only where §20.4's table
licenses it ... Where the table does not license a drop the rewriter MUST
refuse.") So: drop the whole layer (if the layer record's own flags license
a drop) and report the loss, or refuse to rewrite the file at all.

**May it instead re-create the layer?** Only by decoding it — and §20.5 is
explicit that re-creation is decode-then-encode, not copy: "A layer the
rewrite re-creates is new output: its record, its tile-index region and its
stored tiles are written under §20.2's rules from content the rewriter
decoded (§19.3, §19.4), and nothing of the input's copy of that layer is
carried forward." For the genuine W8 premise (a sample type outside the
closed core, which cannot exist in a conforming file in the first place) the
question does not arise; for the on-document case (a tile that fails its
checksum, or a layer under an assigned-but-declined-on-resource-grounds
encoding), re-creation requires exactly the same decode the rewriter could
not do in the first place (that is why it could not verify the tile), so
re-creation is not an available alternative to drop-or-refuse for the
failing tile itself, though the rewriter is always free to re-create
*other* layers it can decode while dropping or refusing over this one.

---

## Legitimate byte-divergence catalogue between two conforming writers

The charter asks for this explicitly; the document states, as a
first-class semantic property (`[R-CNF-05]`): "Writer conformance is
semantic: this specification does not promise canonical bytes, and two
conforming writers given identical input MAY produce different conforming
files." Collecting the specific, named sources of divergence I found across
the document (not an exhaustive enumeration, but every one that is directly
named):

1. **file_id.** Any nonzero u64; only "SHOULD" draw it randomly (§9.3).
2. **Placement of every structure**, absent an alignment/slab declaration:
   "its stored tiles MAY occupy any non-overlapping byte positions, in any
   order" (`[R-SLB-05]`).
3. **Record order within the directory** — "Record semantics MUST NOT
   depend on record order" (`[R-CNT-14]`) — so two writers may emit the
   same records in different sequence.
4. **Slack content** — entirely unconstrained (§5.2): "This specification
   does not constrain the pad's content" and more generally "Slack has no
   internal structure this specification defines, its content is
   unconstrained."
5. **version_minor**, within the floor `[R-CNT-26]` sets (SHOULD the lowest
   defining floor, not MUST) — a writer MAY emit higher.
6. **Codec and filter choice per layer** (§17.2/§17.3) — all four codecs and
   both filters are core and freely selectable; the same decoded tile image
   compresses to entirely different stored bytes under codec 2 vs 3 vs 4,
   or filter 1 vs 2.
7. **Within a chosen codec, encoder-specific bytes that still validate**:
   DEFLATE's final byte's unused high bits (§17.2's Note: "RFC 1951 fixes no
   value for the unused high bits of its final byte ... two files differing
   only in those bits decode to the same tile image and are both
   conforming, which is encoder freedom"); zstd frame parameters not pinned
   by this document (window-size choice below the decoded-size ceiling,
   whether Single_Segment_Flag is set, presence/absence of the optional
   Frame_Content_Size field, §17.2).
8. **User-metadata encoding choice** (encoding 1 verbatim vs. encoding 2
   zstd-compressed, §18.2) for logically identical document content, plus,
   within encoding 2, the same per-frame freedoms as item 7.
9. **JSON number formatting** inside a user-metadata document — explicitly
   named as a non-byte-identity source: "no cross-writer byte-identity,
   since JSON number formatting varies by runtime" (§18.2's closing Note).
10. **Alignment/slab declaration** — a layer MAY or MAY NOT declare either
    (mutually exclusive, `[R-CNT-16]`), freely choosing values within their
    bounds (§16.1, §16.2), changing which bytes are "slack" versus
    "structure" for logically the same content.
11. **Fill-value default**, where the caller does not choose one: "a writer
    whose caller does not choose a fill SHOULD record all-zero bytes. A
    writer that defaults differently still emits a conforming file"
    (`[R-TYP-10]`) — this one is a genuine semantic divergence (it changes
    what unstored samples read as), not merely cosmetic, but it is still a
    named, licensed way two conforming writers diverge on identical caller
    input.
12. **Checkpoint-commit cadence** for a very large single logical write —
    `[R-LIF-07]` (SHOULD, not MUST) — changes the number and placement of
    intermediate directories/trailers in the file for logically the same
    final content.

---

## Findings

See the structured findings list; each is restated in short form here for
cross-reference with the transcript sections above:

- **writerb-01** (the padding-silent fill-change gap, §20.3/§14.5/T4) —
  reasoned out fully under W6 above.
- **writerb-02** (the W11 MU=1/PE=0-from-definition ambiguity) — reasoned
  out fully under W11 above.
