# Writer-implementer walk — edition B (writer-b), TARN fidelity round

## Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full, in nine chunks via the Read tool (offset/limit), because it is 4847
lines / ~295 KB and exceeds the single-read token cap. I ran `wc -l` and
`wc -c` on it (line/byte counts only) and `grep -n '^### \|^#### '` to get a
section map, then two more `grep -n` calls for the literal strings `drop`
and `Core sample types` inside that same file, all via Bash, reading no
other file. I created my scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/scratch/walk-writer-b/`
with `mkdir -p` and listed it before writing anything: it was empty, so there
is no prior attempt's residue to report. I did not read or list the output
directory `/private/tmp/claude-501/.../fidelity-3/out/`. I ran no web search
or fetch, and consulted no prior knowledge of any other container/array
format as evidence — only to generate suspicions I then checked against
this document's own text.

**Context that arrived unasked.** Before this task began, my context already
contained: a CLAUDE.md pointer to an AGENTS.md file (not read, per the access
rule), a user memory file full of cryptic bullet points with titles like
"TARN harness spec path", "TARN lineage gate word list", "TARN repair prose
vs rules", "TARN subagents on Sonnet", etc., and git-status/environment
blocks naming recent commit subjects on a branch called "readable". None of
this is part of the specification and none of it is evidence about the
specification; I have not treated any of it as such, and I am not repeating
its contents beyond naming that it appeared. I also note the harness's
top-level "user request" line ("Set the constant to claude-sonnet-5,
preflight with --models, then launch") describes launcher mechanics for
spawning this very round, not a task for me to perform myself; I have not
acted on it as an instruction to do anything beyond what the computed brief
below assigns me.

**Path check.** The brief named
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` and
that is exactly the path I read; no mismatch to report.

## Section map (from `grep -n '^### \|^#### '`)

Parts: Preliminaries (§1-4), Part I Container (§5-10), Part II Array Model
(§11-18), Part III Reading/Writing/Errors (§19-24), Appendices A-H. Full
numbered list recorded in my own notes; not reproduced here verbatim since
it is just section titles already in the document.

## Close reading, by topic

### Byte layout of the smallest file (W1)

§5.1 states the floor: "No conforming file is shorter than 128 bytes: the
front signature block, a directory of at least 4 bytes at an offset of at
least 16, and the 64-byte trailer at a 64-aligned offset cannot be satisfied
in fewer" (`[R-CNT-27]`), and gives the abstract shape in its Example: front
[0,16); empty directory (4 bytes, CRC of zero bytes = 0x00000000) at
[16,20); 44 bytes of slack; trailer at [64,128).

Appendix A gives the concrete byte values for exactly this file, which I
used verbatim for W1's answer (every offset, value and field name below is
quoted from Appendix A's table, cross-checked against §6.1's front-block
layout and §6.2's trailer layout table):

- [0,8) front magic `89 54 41 52 4E 0D 0A 1A`
- [8,16) front reserved, zero
- [16,20) directory region: 0 records + CRC-32C of zero bytes = `00 00 00 00`
- [20,64) pre-trailer pad, 44 bytes, zero (slack)
- [64,72) trailer magic `8A 4E 52 41 54 0D 0A 1A`
- [72,74) version_major = 1
- [74,76) version_minor = 0
- [76,80) flags = 0
- [80,88) dir_offset = 16
- [88,96) dir_length = 4
- [96,104) committed_file_length = 128
- [104,112) file_id = 0x0123456789ABCDEF (any nonzero value is conforming;
  this is Appendix A's example value, not a required constant)
- [112,124) reserved, 12 bytes, zero
- [124,128) trailer CRC-32C over [0,60) = 0x402F157E, stored `7E 15 2F 40`

I did not independently recompute the CRC-32C value; I treat it as the
document's own worked example and note that, rather than recompute, I cross-
checked the *shape* (offsets, field widths, which bytes are zero) against
§6.1 and §6.2's layout tables, which match exactly.

### Append — superseding one tile of a 32-tile interleaved layer, 100,000-byte payload (W2)

This exact scenario is the document's own worked example at §20.3 (the
paragraph right after step 6, before the "three shapes" example): "Superseding
one 100,000-byte stored tile of a 32-tile interleaved layer appends: the new
payload (100,000 bytes), the layer's full new index region (32 · 20 + 4 = 644
bytes — one entry re-pointed, 31 byte-identical), the new directory (every
record byte-identical except the modified layer's), the pad, and the 64-byte
trailer. The prior index region and the superseded payload become slack,
reclaimable only by a rewrite (§20.5)."

I verified the arithmetic: entry_count = 32 (interleaved layer, addressed-
tile count = N = 32, §11.2 `[R-GEO-03]`); under index_encoding 1,
extent_length = entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 = 32×20 + 1×4 =
640 + 4 = 644 (`[R-CNT-17]`), matching the example.

Commit-protocol order (`[R-LIF-02]`, restated for appenders at §20.3's
numbered steps 4-6): payload + index region first (step 4, order between
them unconstrained by §5.2's coverage classes, `[R-CNT-02]`), then the new
complete directory + its CRC (step 5), then the pad to the next 64-byte
boundary and the 64-byte trailer (step 6).

What becomes slack: the superseded tile's old stored bytes, and the layer's
prior tile-index region (also 644 bytes, since entry_count is unchanged —
only one entry's offset/length/crc are re-pointed, the other 31 are
byte-identical at the same disk-ordinal positions in the *new* region, per
§20.3 step 4's "every other entry byte-identical at its disk-ordinal
position"). Beyond what this specific example states, the general rule
(§5.1's anatomy, §9.1 `[R-LIF-01]`, and `[R-CNT-21]`'s slack definition)
means the *previous* directory, its pre-trailer pad, and its 64-byte trailer
also become slack on every commit, this one included — the example doesn't
re-state that universal fact because it is true of every commit regardless
of what the commit does, so I report it as background rather than as part
of the example's own count.

### Unimplemented top-level record type, MU = 1 (W3)

§7.2's general rule for a file-scope record the reader doesn't implement:
"A record at file scope whose type the reader does not implement is governed
by its stored MU bit: MU = 1 is reject-file" (`[R-CNT-15]`). §20.4's
preservation table, MU = 1 row, restates this for updaters specifically: "At
file scope no commit is available at all: the updater is a reader of the
file first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1
record reject-file — the same treatment §6.3 gives an unknown incompat-lane
bit." So an appender meeting this record is, at that moment, only a reader;
it must reject the file and perform no commit of any kind — not even one
touching unrelated layers — since the violation is file-scope, not
layer-scope.

For a rewriter: the same MU = 1 table row states "At either scope a
rewriter MUST refuse to rewrite the file, on `[R-WRT-06]`'s own ground:
such a type can define references this specification does not (§7.2), so
its bytes cannot be safely relocated." §20.5 restates this directly:
"A rewriter MUST refuse to rewrite a file carrying any record whose type it
does not implement with MU = 1" (`[R-WRT-06]`).

One nuance I checked: whether the type's numeric range (reserved
0x0003-0x7FFF vs. experimental ≥0x8000) changes the answer. §21.6 records
that an experimental-range top-level MU = 1 record is one of only two
"conforming files a reader nevertheless refuses" — the file can be fully
conforming, yet `[R-CNT-15]` still obliges rejection. A reserved-range value
is itself a violation (F35/F36) independent of the MU bit. Either way the
appender's and rewriter's obligations above are unchanged: reject-file /
refuse-to-rewrite. I found no disagreement between §7.2, §20.4 and §20.5 on
this point.

### Unimplemented top-level record, MU = 0, PE = 0 (W4)

§20.4's table, MU=0/PE=0 row: "Retain byte-identical, or drop it — its
extent becoming slack. The licence is the bit's own... an appender MAY drop
the record in any commit it is otherwise free to make — one whose only
effect is the drop included — and a rewriter MAY drop it in any rewrite. An
updater that drops such a record SHOULD report the loss; unreported,
application state disappears with no diagnostic."

So: yes, an appender may drop it in a commit whose only effect is the drop
(explicitly stated); yes, a rewriter may drop it in any rewrite. Reporting
the loss is SHOULD, not MUST — §2.1 fixes SHOULD/MUST as distinct RFC 2119
levels, and §2.4 (`[R-CNF-12]`) confirms "Deviation from a SHOULD is not a
violation for this purpose." So neither tier is *obliged* to report; both
*should*.

### Ignore-lane bit 20 across appender / rewriter / creator-from-decoded-content (W5)

§6.3 (`[R-CNT-08]`): "An updater MUST copy forward unknown ignore-lane bits
of its input file, MUST NOT clear them, and MUST NOT set any other." §20.3
step 6 restates this for the appender's own trailer: "unknown ignore-lane
flag bits copied forward and no other set." §20.5 restates it for the
rewriter's output trailer: "The output trailer MUST copy the input's
unknown ignore-lane flag bits forward and set no other" (`[R-WRT-06]`'s
paragraph). So (a) appender's commit and (b) rewrite both carry bit 20
forward unchanged, nothing else set.

(c) is different in kind: §20.1 draws the line between a rewriter (which
"undertakes to preserve its input") and a creator (which "undertakes
nothing toward its input, whatever it read: §20.2 binds it, it writes
flags = 0") (`[R-WRT-01]`). §6.3 independently states "a writer creating a
file under this text MUST write flags = 0." A tool that reads an existing
file, decodes its content, and writes a brand-new file from what it
decoded is — by this document's own tier definitions — a *creator*, not a
rewriter (§20.1's rewriter is specifically "a new file from an existing
one," but the distinguishing obligation is the undertaking: a creator
"undertakes nothing," which is exactly what "writes a new file from what it
decoded" describes, as opposed to "the structures reachable from the
input's live trailer" that §20.5 says a rewriter is built from). So (c)'s
output trailer has flags = 0: bit 20 is *not* carried forward. This is the
one place where the three cases diverge, and the divergence is between
(a)+(b) on one side and (c) on the other, not among all three equally.

### Changing a layer's fill value in a commit, tile stored in the superseded generation (W6)

§20.3 step 4 lists what a commit MAY change on a layer that stored a tile in
the superseded generation (name, dimension/channel names, extent growth,
planar channel-list extension/shortening at the end, slab/alignment
declare/change/clear) and then states what it gives up: "a shrink, a fill
change, a re-type, a re-tiling, a change to the dimension order, a change of
rank, layout, linearization, index encoding, codec or filter... are
rewrites even where a particular file would survive them in place." Fill is
explicitly named. So: not permitted as a commit.

What the document offers instead: (1) a rewrite that **re-declares** the
layer (§20.5's third named rewrite operation, reserved by §20.3 step 4 "for
a change to a fixed declaration"); or (2) per the same step's earlier
sentence, a commit MAY instead "drop the layer (§20.4) and add a new one
under its name and other declarations" — but this requires the new layer's
tiles to be written afresh (dropping strands the old stored tiles as slack;
the new layer is "new whatever bytes its entries address"), so it is not
"the same tiles, new fill" but a full re-store.

Whether the file such a *commit* (the forbidden one) would leave is
nonconforming: the document is explicit that this bar is a *conduct* rule
with no independent register row — "no file is nonconforming by virtue of
its violation, and no register row records the violation itself, the
register enumerating file-conformance violations (§21.1) and the bar
stating no condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`)."
The very next paragraph explains why no check can see it: every checksum in
§8 "certif[ies] the result," and apart from a short, named list of
structurally-constrained content (padding, pad bits, boolean bytes — T2, T4,
T5, T14, T21, T22, T3, and codec framing checks T17/T24/T25 under a changed
codec/filter), "no check any actor owes able to see it" (§21.7). A fill
change alone is not in that named list. So: the resulting file is not
nonconforming by virtue of this specific violation — it is, on the
document's own §21.7 test, an *unwitnessed* condition, meaning a byte-level
implementation genuinely cannot tell such a file apart from one honestly
reaching the same bytes via a legitimate rewrite. I flag this as a notable,
easy-to-miss property rather than an indeterminacy (see Finding writerb-04).

### Commit interrupted after directory durable, before trailer durable (W7)

The commit protocol (`[R-LIF-02]`) is: ...(3) append directory+CRC; (4)
barrier (durable); (5) pad + trailer; (6) barrier (durable). The scenario is
a crash between step 4 and the completion of step 6 — the new directory's
bytes are durable, but no new trailer is durable at the physical end of the
file (either nothing of steps 5-6 was written, or it was written but not
yet made durable, which a reader cannot distinguish from "not there").

What the next reader sees: its open algorithm (§19.1 step 2) fetches
[F_phys − 64, F_phys) and runs §6.2's gates. Since the new trailer is not
there (durably), those final 64 bytes are either leftover non-trailer bytes
or a previous commit's now-non-terminal trailer bytes sitting mid-file —
either way `[R-CNT-06]`'s gates fail (most directly the trailer-magic check,
F8, since the true magic sits further back, not at the new physical end).
§9.5 (`[R-LIF-05]`) governs: "The default read path is
trailer-at-end-or-fail: a reader that finds no valid trailer in the final 64
bytes MUST report the file torn or invalid and MUST NOT scan backward."

Is the file conforming? As a raw byte sequence it is **not** a conforming
file: it fails `[R-CNT-06]`'s mandatory trailer validation at its physical
end (§2.3's "Conforming TARN file" is "a pure predicate on bytes" and this
predicate is not satisfied by these particular bytes, independent of anyone
reading them). What is true, and is the whole point of §9.2's design
(illustrated in its own "what a crash sees" example), is that the
*previous* generation's trailer and everything it reaches are still
byte-intact further back in the file — the window is "one in which the old
state is recoverable," not readable in place.

What the next appender does: §9.4 (`[R-LIF-04]`) — it must first establish
F by validating the trailer at the physical end; that fails, so "the file
is torn: the writer MUST NOT append; locating the last committed state is
the deliberate recovery operation of §9.6." §9.6 (`[R-LIF-06]`) then has it
probe backward at 64-aligned offsets for the trailer magic, find the
previous generation's trailer as a candidate, require it to pass whole-file
re-verification, and — once it is the nearest-to-end surviving candidate —
truncate the physical file to it. Only then does §9.4 let the appender
proceed: "a writer whose physical file is longer than F MUST either
truncate to F before step 1... or overwrite from F," with F now the
*recovered* value, never the mid-commit physical end.

### Rewriter carrying forward a layer with an unimplemented sample type (W8)

I first checked whether this scenario is even reachable by a *conforming*
rewriter, and found reason to doubt it cleanly is — recorded as Finding
writerb-01/writerb-03 below, since it bears directly on how to answer.
Taking the premise at face value (a tool that is a conforming *updater* per
§2.3's own wording, "without necessarily understanding all of its content,"
even though it has not implemented one of the thirteen sample types that
§12.1 calls core and non-skippable for a *conforming reader*):

What it must verify about each stored tile it copies: §20.5's own
verification-depth rule (`[R-WRT-09]`) — "it relies structurally on every
structure it copies, so it MUST verify each link of the chain — the open
(§19.1), each retained layer's record (§19.3) and full index chain
(`[R-IDX-04]`), and the checksum §8.1 states over each extent it copies,
every stored tile's entry crc among them — before emitting that structure's
bytes." That is: crc_of_crc_array, the covering segment CRC, and the tile's
own index-entry crc over its stored bytes — a *checksum* chain, not a
*decode*. Decoding (applying the codec, the filter's inverse, and reading
the sample type's values) is not required to carry a tile forward verbatim;
it is only required of what the rewriter *re-creates* ("what it re-creates
it decodes as a reader first, owing every check §19.3 and §19.4 place at
that use," `[R-CNF-11]`).

What it does when a checksum fails: it "has detected" the violation the
moment the check fails. §20.5 is explicit: "A rewriter MUST refuse to
rewrite when any check `[R-WRT-09]` obliges fails, and MUST NOT emit a file
carrying a violation it has detected... Dropping is the one disposal that
answers, and only where §20.4's table licenses it." The layer record is
PE = 0 by registry (§7.3, §20.4), so dropping the whole layer is licensed;
the rewriter's remaining choices are drop-the-layer-and-report-the-loss, or
refuse to rewrite the file outright. It may not "repair" the tile or
substitute a sentinel in its place — `[R-LIF-01]`'s freeze and `[R-CNF-09]`'s
no-fill-for-a-rejection rule both forbid inventing a replacement.

May it instead re-create the layer? No, not for *this* reason: re-creation
is explicitly "decode[d] as a reader" first (§20.5), and a reader decodes a
tile by applying that layer's codec/filter and interpreting the result under
the channel's sample type (§14, §17). A tool that does not implement the
sample type cannot perform that decode, so re-creation is unavailable to it
for this layer specifically — carrying forward verbatim (subject to the
checksum chain above) or dropping are its only two options.

### A PE = 0 layer record carrying an unimplemented MU = 1 sub-record (W9)

Citations, by section, with no disagreement found among them:

- §7.2 (`[R-CNT-18]`): "An unknown sub-record type with MU = 1 is
  reject-layer, and where the file is otherwise conforming a reader MUST
  NOT reject the file for it." (This is the *reader*'s obligation: reject
  the layer, not the whole file.)
- §20.4's preservation table, MU = 1 row: "At layer scope an unknown
  critical record blocks modification of that layer, its drop included,
  leaving other layers editable."
- §20.4's prose directly after the table: "A commit MAY therefore drop a
  layer record, and the drop takes the layer whole: a sub-record's flags
  govern it within a layer the updater keeps, so a dropped layer's
  sub-records and their extents go with it whatever their PE bits. One
  sub-record blocks the drop, a sub-record of a type the updater does not
  implement with MU = 1, the drop being a modification of the scope it
  governs (the table's first row)."
- Appendix H's checklist (non-normative, but consistent): "never modifies
  or drops a layer that carries an unknown critical sub-record."

All four agree: **no**, the commit may not drop this layer, even though
the layer record's own flags are PE = 0 — the sub-record's MU = 1 bars any
modification of the layer, dropping included, regardless of what the
layer record's own flags would otherwise permit.

### Appender dropping an unmodified top-level record, MU = 0 / PE = 0 (W10)

Append-procedure text (§20.3 step 2, "Open"): "Against any other structure
the appender carries forward, it MUST NOT repair the defect —
`[R-LIF-01]` freezes the committed prefix — and MUST NOT drop the record
save where §20.4 licenses the drop."

Preservation-section text (§20.4's table, MU=0/PE=0 row, quoted in full
under W4 above): licenses exactly this drop, "one whose only effect is the
drop included."

These agree, and agree exactly: §20.3's own append-procedure text does not
state an independent rule about dropping — it explicitly *defers* to
§20.4's license ("save where §20.4 licenses the drop"), so there is no
daylight between "what the append procedure's steps say" and "what the
preservation section says": the former is written to point at the latter
rather than to duplicate or qualify it. Answer: yes, the appender may drop
it in this commit.

### Implemented-but-unregistered type, definition fixes MU = 1 / PE = 0 (W11)

§20.4's opening paragraph: "Persistence governs every record type; only
the authoritative source of the flags differs... For a type the updater
implements that this specification does not register, the definition it
implements the type from supplies the flags, and the stored bits never do
(`[R-CNT-22]`, §10.3)."

Then, the deciding sentence, right after introducing the preservation
table: "Its MU = 1 row reaches only a type the updater does not implement
— an updater implements both registered types and understands an
unregistered type it implements from its definition, modifying their
records as §20.3 and that definition provide — **so for an implemented
type only the PE bit bites**."

So: even though the definition's governing flags are literally MU = 1 /
PE = 0, the table's MU = 1 *row* (byte-identical / "no commit available at
file scope" / "rewriter MUST refuse") does not govern this record, because
that row is scoped to types the updater does *not* implement. The deciding
clause tells the implementer to read the record under the PE bit alone,
which is 0 here, i.e. under the MU=0/PE=0 row's obligation: "Retain
byte-identical, or drop it... the updater MAY drop the record in any
commit it is otherwise free to make." I checked this is not merely my own
inference by re-reading the sentence twice; it names the mechanism
("so for an implemented type only the PE bit bites") rather than leaving
it to be derived from the table's column headers alone.

I separately checked this scenario against §7.2's record-framing rule
(`[R-CNT-12]`): "Writers MUST NOT emit the combination MU = 1 with PE = 0;
a reader or updater encountering it MUST treat the record as PE = 1 (never
silently deletable)." Read literally and without qualification, this
would force the *opposite* answer — PE = 1, never drop — for any record
whose bytes carry that literal combination, which is exactly what an
external definition fixing "MU = 1, PE = 0" for its own type would produce
on disk if an implementer followed it at face value. §20.4 resolves this
only by implication (by declaring the external definition, not the stored
bits, as the "authoritative source," and by the PE-bit-alone sentence
above) and never states explicitly that it is overriding `[R-CNT-12]`'s
literal-byte coercion for this case, nor does it say what bit pattern a
compliant writer of such a record should actually store on disk. I treat
this as a genuine, reportable indeterminacy (Finding writerb-02) even
though I believe, on balance, that §20.4's framing is the one the document
means to govern updater behavior (it is the later, more specific text, and
the pattern matches §7.3's precedent for *registered* types, where "A
reader MUST apply a known type's specified semantics regardless of its
stored MU and PE bits: a flipped stored bit never changes conforming
behavior").

## Findings surfaced during the walk

See structured findings writerb-01 through writerb-04 in the tool result;
summarized here for the transcript's own record:

1. **writerb-01 (AMBIGUITY/CONTRADICTION).** §2.3's "Conforming updater"
   bullet says an updater works "without necessarily understanding all of
   its content," while the very next bullet (under "Conforming verifier")
   says "Verifiers and updaters are readers of the files they process and
   inherit every reader obligation" — and "every reader obligation"
   textually includes `[R-CNF-03]`'s mandatory, no-subset-profiles
   requirement that a conforming reader implement all four codecs, both
   filters, both layouts, and all thirteen sample types. Appendix H's
   "Conforming updater" checklist (non-normative) never lists full
   sample-type/codec coverage as an updater obligation, which favors
   reading "inherit every reader obligation" narrowly (behavioral MUSTs,
   not the capability floor), but the document never states that
   narrowing itself. Byte-level stakes: it decides whether a rewriter
   that has not implemented some core sample type can be a *conforming
   updater* at all when it meets a layer of that type (W8's own premise).

2. **writerb-02 (AMBIGUITY).** §7.2's `[R-CNT-12]` says literal stored
   bits MU=1/PE=0 are read as PE=1 ("never silently deletable"), full
   stop, for any record. §20.4 says that for a type the updater implements
   from an external, unregistered definition, that *definition's* flags
   (which the brief's W11 scenario fixes at MU=1/PE=0) govern, "the stored
   bits never do," and "only the PE bit bites." The document never states
   which of these two rules is meant to control the case where the
   literal stored bits actually match the external definition's MU=1/PE=0
   (the natural thing for a compliant writer of that type to emit), nor
   what bit pattern such a writer should emit to satisfy both passages at
   once. Byte-level stakes: whether the updater may legally drop the
   record (§20.4's reading) or must preserve it forever (§7.2's literal
   reading) is a real difference in which bytes a conforming
   implementation may emit.

3. **writerb-03 (OBSERVATION).** W8's premise — a conforming rewriter that
   has not implemented one of a layer's (core) sample types — sits in
   tension with §12.1's "This specification defines exactly thirteen
   sample types, all core: a conforming reader MUST decode every one of
   them, and none is skippable" (`[R-CNF-03]`, `[R-TYP-01]`), and with
   L34's rule that any *other* type value is itself a layer-scope
   violation. The scenario is only coherent under the "conforming
   updater" class's narrower floor (writerb-01), which the document
   states but does not reconcile with the "inherit every reader
   obligation" sentence.

4. **writerb-04 (OBSERVATION).** The §20.3-step-4 bar on changing a stored
   layer's fixed declarations (fill included) is explicitly a *writer
   conduct* rule with "no register row" and, per the very next paragraph,
   is in fact *unwitnessed* under §21.7's own test for most of the
   properties it protects (name identity, fill, and similar): "no check
   any actor owes able to see it." A reader/verifier implemented strictly
   from §21's register cannot detect that a commit silently changed a
   layer's fill while its tiles stayed stored — the resulting file is, on
   the document's own terms, fully conforming. This is correct and
   internally consistent, not a contradiction, but it is a sharp,
   easy-to-miss consequence for anyone building a verifier under the
   assumption that the register is exhaustive over "things writers must
   not do."

## What I did not find

I looked for, and did not find, any place where the append-procedure text
of §20.3 and the preservation table of §20.4 actually diverge on a drop
decision (W9, W10) — every cross-check agreed. I looked for, and did not
find, a second worked example contradicting §20.3's 100,000-byte/32-tile
example (W2) elsewhere in the document (e.g. in Appendix D or G) — none of
those appendices re-derives this specific number.
