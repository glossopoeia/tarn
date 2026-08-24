# Refute-only transcript — G2 (carried-over-actors): X-05, A-05

## 0. Disclosure of what I read and ran

Read in full:
- /private/tmp/.../r23audit/refute/finding-X-05.md
- /private/tmp/.../r23audit/refute/finding-A-05.md
- /private/tmp/.../r23audit/hunk-01.diff
- /private/tmp/.../r23audit/hunk-02.diff
- spec/tarn.md, by `sed -n` ranges: 100-260, 2240-2320, 2430-2530, 3290-3400,
  3520-3546, 3556-3640, 3640-3760, 3762-3800.

Ran (greps against spec/tarn.md only):
- `grep -n "no codec's embedded size"` -> 3776
- `grep -n "allocat"` -> 406, 449, 1920, 2290, 2353, 3765, 3772, 3776, 3779, 3781
- `grep -n "dictionar\|Dictionary"` -> 2232, 2276, 2277, 2278, 2279, 2464, 3511, 3546, 3614
- `grep -n "detectab\|undetectab"` -> 227, 1102, 2280, 2282, 2382, 3300, 3310, 3311, 3518, 3636
- one python3 script reading only spec/tarn.md, counting register rows and
  semicolon-separated instance cells.

Not read: docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, full.diff, hunks 3-4, other
auditors' briefs, the web. I did not list the r23audit directory.

**Unrequested context that appeared before I began:** a project instruction
file naming another file, and an index of maintainer memory notes with
filenames and one-line descriptions. I opened none of them and drew nothing
from them. Their contents are not repeated here.

## 1. The instance arithmetic, checked first (cheap, and adjacent to hunk 2)

Hunk 2 added 4 instances to R4 (12 -> 16). §21.8 [R-ERR-02] asserts
"121 conditions over 277 instances".

Script output: `rows 121 instances 277`, by family
F 36 rows / 58 instances, L 49 / 116, T 26 / 55, R 10 / 48; R4 = 16 instances.
§21.5's preamble says "10 conditions" — matches.

So the totals were carried through with hunk 2. No stale-count defect here.
Also checked against §21.1's direction rule ("Where the condition compares two
**magnitudes** either of which can be the greater — a *differs from* or *does
not equal* — the two directions are likewise enumerated"): §18.2's content-size
rule is an equality, so larger + smaller × 2 containers = 4. Correct.

## 2. The charter's sort: every item on the carried-over list, by actor and witness

§18.2 (2461-2467), verbatim:

> Carried over — named for convenience, not as a closed list — are the frame
> magic; no skippable frame and no second frame; no dictionary use, disclosed
> or not, and no nonzero dictionary ID; no content-checksum flag; and the bar
> on sizing any buffer from a length the frame itself declares.

| item | actor bound | single-file witness? | R4 instance? |
|---|---|---|---|
| frame magic | file/writer, reader detects | yes (first 4 bytes) | yes ×2 |
| no skippable / no second frame | file/writer, reader detects | yes | yes ×4 |
| no dictionary use, **disclosed** | writer | yes — via nonzero Dictionary_ID | via next row |
| no dictionary use, **undisclosed** | writer conduct | **no** | **none** |
| no nonzero dictionary ID | file/writer, reader detects | yes | yes ×2 |
| no content-checksum flag | file/writer, reader detects | yes | yes ×2 |
| bar on sizing any buffer from a declared length | **reader** | **no** | **none** |

Two misfits, and they are exactly the two X-05 names. R4's row is
`| ... | reader | extent use | [R-MTA-09] (R-COD-06, R-CNT-25) |` — detector
reader, detection point extent use, outcome ignore-record (§21.5's heading).
Neither misfit item can be detected by a reader at extent use, or by anyone.

Old text for comparison (hunk 1, "-" side): the import was closed and narrower —
"under the frame constraints of `[R-COD-06]` that do not reference a tile: the
frame magic; no skippable frame and no second frame; no nonzero dictionary ID;
no content-checksum flag." Neither misfit was in it. The repair introduced both.
So the finding's premise — that the widening put these two inside R4's reach —
is factually right about the change.

## 3. X-05 leg 3 (the "save two" overlap) — refuted on the text

Auditor: exception (b) is an instance of exception (a) because [R-COD-06]'s
window clause reads "MUST NOT declare a window size exceeding the tile's
decoded size".

[R-COD-06] makes a *second* Window_Size statement the auditor omits
(spec/tarn.md 2292-2296):

> Writers SHOULD keep the declared window within §21.9's 8 MiB `Window_Size`
> guarantee even for a larger tile; a wider window is conforming and merely
> permits a conforming reader to decline the tile or the layer on resource
> grounds (`[R-ERR-04]`). `[R-COD-06]`

"even for a larger tile" is explicit that this clause is not indexed on the
tile's decoded size. So (b) carries content (a) does not, and §18.2's window
paragraph rebuilds precisely that second half ("a reader's window bound is its
own, no smaller than §21.9's guarantee for that quantity ... the file exceeds a
§21.9 guarantee and so remains conforming while the reader MAY decline it").
Two distinguishable subject matters, both replaced. Leg 3 fails.

Even had the overlap existed: both exceptions are replaced by §18.2 in the same
breath, so an overlap between them would be redundancy, not divergence. No
byte can turn on it.

## 4. X-05 leg 2 / A-05 (the buffer-sizing bar) — real misfit, not byte-level

R4's grammatical subject (3546): "A user-metadata **document** stored under
encoding 2 **breaks** one of the frame constraints ...". A document does not
allocate. The bar is a vacuous member of R4's quantified set. It contributes no
condition, no instance, no outcome, no detector assignment.

A-05's added claim is scope: [R-COD-06] bars sizing "from **it**" (the frame
content-size field, 2290-2291); §18.2 restates it as "a length the frame itself
declares", which also reaches Window_Size and every Block_Size.

Constructions I built to try to make the widening byte-level:

(a) **Window_Size, reader admits it.** Frame declares Window_Size = 4 MiB,
reader's bound is the §21.9 floor of 8 MiB. Narrow reading: reader may allocate
4 MiB. Broad reading: reader must allocate its own 8 MiB bound. Both decode the
same document, return the same document, accept. No byte, no verdict.

(b) **Window_Size, reader does not admit it.** Frame declares 16 MiB, bound
8 MiB. §18.2: "a frame declaring more than the reader admits is ignore-record
on that ground". That is a *comparison*, not a *sizing*; the broad bar does not
forbid it, and §21.5's preamble expressly preserves it ("except where a reader
or verifier declines the decode on the size bound or on the frame's declared
window"). Identical under both readings.

(c) **Block_Size.** Broad reading forbids sizing a block buffer from a block
header's declared size. RFC 8878 caps Block_Maximum_Size at
min(Window_Size, 128 KiB), so a reader allocates that unconditionally and
decodes identically. Awkward as an implementation-technique constraint (which
the §2.1 Note disclaims), but no byte moves.

(d) **The content-size field.** Both readings cover it, so no divergence — and
here the carry-over is *load-bearing*, which cuts against A-05's premise that it
was a careless widening. Hunk 1 routed a content-size mismatch to R4, which
requires the reader to learn the decoded length. Without the bar, a reader
facing content-size = 20 MiB with its own 16 MiB bound could size from the
declared field, decline on the bound, and report a capability decline
(§21.5: "not a fact about the file"), while a reader obeying the bar decodes to
1 KiB, finds the mismatch, and records an R4 violation. **That** would be a
verifier-verdict divergence — *cannot establish* versus *nonconforming* — and
the carried-over bar is what forecloses it. The repair closes a divergence here
rather than opening one.

(e) A-05's own harm scenario ("allocate your full bound unconditionally is the
only compliant behaviour") is what §22.2 [R-SEC-02] already prescribes, in
normative body prose, generically, citing the same rule (3775-3777):
"the reason no codec's embedded size field is ever an allocation source
(`[R-COD-06]`)", and (3780-3784) "A reader MUST NOT size an allocation, fetch,
or index walk in proportion to a declared magnitude it has not corroborated
against the file's actual length." I confirmed by `grep -n allocat` that lines
3765-3784 are the §22.2 block and carry no ">" prefix, and by [R-CNF-01]
(104-106) that §22 is not an excluded class. So the document already reads the
bar generically. A-05 is answered inside the specification.

A-05: **REFUTED, not byte-level.** Downgrade stands.

## 5. X-05 leg 1 (the undisclosed dictionary) — real, and *not* refuted by the
document, but still not byte-level

The verifier's refutation runs: §18.2 imports the *rule*, so [R-COD-06]'s own
carve-out (2279-2283) travels with it; and §21.1's arbitration ("where a row and
the rule it cites diverge, **the rule governs**") sends R4 back to [R-COD-06].

I tested that chain and it does not close.

§21.1 (3303-3306) fixes what "the rule it cites" means:

> A Governing rule cell names that requirement first; any identifiers following
> it in parentheses are the further rules the condition reads, cited without
> brackets to keep them distinct from the governing one.

R4's cell is "`[R-MTA-09]` (R-COD-06, R-CNT-25)". The **governing** rule is
therefore [R-MTA-09] — §18.2 — not [R-COD-06]. And R4's condition text tracks
that: "breaks one of the frame constraints **§18.2 states** or carries over from
`[R-COD-06]`". "No dictionary use, disclosed or not" is a constraint §18.2
*states*, in its own words, with no detectability qualifier attached. So the
arbitration rule the verifier invokes routes to the text that did the widening,
which says nothing about undetectability. [R-COD-06]'s carve-out is a sentence
about a *tile* ("Dictionary use the header does not disclose ... it is a writer
violation whose consequence is wrong decoded content"), and it is an accounting
statement about a constraint rather than a constraint the import can carry.

Nor does §21.7 close it. Its first paragraph names the undisclosed dictionary
under `[R-COD-06]` (3613-3615) — the tile case. Its second paragraph is the
enumerated list of obligations "omitted from the register because a single file
exhibits no witness of their violation", and I read it in full (3624-3663): it
names [R-LIF-01], [R-LIF-03], [R-GEO-06], [R-SER-01], [R-CNT-13], [R-CNT-18],
§20.3 step 4, [R-WRT-06], [R-ENC-06]. **[R-MTA-09] is not in it**, and neither
new carried-over item is. §21.1 (3310-3313) makes that list the operative
account: "detectability being the gate `[R-CNF-07]` already applies and §21.7
the account, by class, of what fails it". So by §21.1's own terms, a constraint
§18.2 states, that fails the detectability gate, and that §21.7 does not
account for, is a gap the document leaves open.

**So X-05 leg 1 is a real defect and is answered nowhere in spec/tarn.md.**

### Is it byte-level? I could not make it one.

The property "this frame was compressed against an undisclosed dictionary" is
not a predicate on the frame's bytes at all — [R-CNF-02] defines file
conformance as "a pure predicate on bytes", and the same byte sequence can be
produced with or without a dictionary whenever every match offset lies inside
the frame's own output. Constructions:

- **Writer side.** Under the current text and under X-05's proposed repair,
  §18.2 bars dictionary use either way (as a registered constraint, or as a
  flagged writer-conduct rule). [R-CNF-05] binds the writer identically. The
  emittable set does not move.
- **Reader side.** Undetectable by construction. Same accept/ignore-record.
- **Verifier side.** Undetectable; §21.7's closing sentence (3620-3623) gives
  the verdict either way — "no file-level witness exists to check, so nothing
  about the file is left undetermined and the verdict is unaffected."
- **Updater side.** §20.4 preserve-verbatim carries the extent forward without
  the updater being able to know. Identical under both readings.
- **The one case where dictionary use *is* witnessed**: a frame whose first
  match offset exceeds the bytes decoded so far can only have been produced with
  a dictionary/prefix, and a decoder without it fails. That file is already R3
  ("stored bytes fail to decode under its declared assigned encoding") —
  ignore-record, reader, extent use. R4 would fire too. §21.1 sends a
  specialization to the narrower row and both rows carry the same outcome, so no
  reader and no verifier diverges. Corpus unaffected: R4's instance cell names
  no undisclosed-dictionary instance, and R3's cell is unchanged at 2.

I also checked the neighbouring guarantee composition, in case the widening had
knocked it loose: a 12 MiB document written as a single-segment frame derives
Window_Size = content size = 12 MiB, exceeding §21.9's 8 MiB row while lying
inside the 16 MiB document row. [R-CNF-03]'s acceptance duty is conjunctive
("none of whose values exceeds the minimum guarantees"), so the duty lapses and
the reader MAY decline. No conflict, and in any case untouched by hunks 1-2.

## 6. Verdict

- **A-05** — refuted. The widening is either not a widening (§22.2 [R-SEC-02]
  already states the general bar, citing [R-COD-06]) or is load-bearing for the
  content-size routing hunk 1 introduced. Not byte-level.
- **X-05** — legs 2 and 3 refuted. **Leg 1 survives as a real documentation
  defect**: §18.2 now states an undetectable writer-conduct constraint, R4's
  condition text sweeps in "the frame constraints §18.2 states", §21.1 confines
  the register to detectable violations and makes §21.7 the account of what
  fails that gate, and §21.7 does not account for this one. The reasoning that
  would answer it is not in the document. It is **not byte-level**: no
  construction moves the emittable set or any accept/reject verdict, because the
  property is not a property of the bytes.

Verdict: **DOWNGRADE_STANDS** (no finding in this group moves the emittable
set), with X-05 flagged as a surviving non-byte-level defect and a missing
sentence named.
