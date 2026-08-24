# Repair audit — hunk-01 (§18.2 encoding-2 passage) and hunk-02 (§21.5 row R4)

## 0. Disclosure

Read, in full or in the ranges named:

- `/private/tmp/.../r23audit/hunk-01.diff` (my charter hunk)
- `/private/tmp/.../r23audit/hunk-02.diff` (my charter hunk)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, ranges:
  140–235 (§2.3 R-CNF-02/03/04/05/06/11), 258–290 (§2.4 R-CNF-12, §2.5
  R-CNF-10), 950–985 (R-CNT-14/15), 2240–2380 (§17.2 R-COD-03..R-COD-08 and
  their Notes), 2380–2560 (§17.3, §17.4, §18.1, §18.2 in full), 2556–2600
  (§18.2 close, R-MTA-10, §18.3 opening), 2735–2755 (§19.2 R-RDR-02),
  3290–3400 (§21.1 and §21.2 head), 3515–3560 (§21.4 tail, §21.5 in full),
  3554–3608 (§21.6 in full), 3600–3680 (§21.6 close, §21.7, §21.8, §21.9
  head), 3680–3760 (§21.9 limits table, R-ERR-03, R-ERR-04, R-ERR-05),
  3820–3840 (R-SEC-04), 4388–4412 (appendix verifier checklist).

Ran (all against `spec/tarn.md` only):
- `grep -n "R-COD-06"`, `grep -n "R-MTA-09\|R-MTA-10\|R-CNF-02\|R-ERR-04\|R-CNF-10\|R-CNF-11\|R-COD-11"`,
  `grep -n "content-size\|content size\|Frame_Content_Size\|Window_Size\|window size\|window bound"`,
  `grep -n "^#### 21"`.
- A python3 whitespace-normalising search over the whole file (the document is
  hard-wrapped, so I collapsed all runs of whitespace to single spaces before
  matching) for: "failure to decode" (2 hits), "fails to decode" (1),
  "fail to decode" (1), "decoder's tolerance" (1), "checkable from the bytes
  alone" (1), "carries over from" (1), "named here or not" (1), "disclosed or
  not" (1), "sizing any buffer" (1), "allocate or size any buffer" (1),
  "dictionary" (all hits printed with 260 chars of context each).
- A python3 count of every §21.2–§21.5 row and its semicolon-separated
  instances: **121 rows, 277 instances**; per family F=58, L=116, T=55, R=48;
  R4 = 16 instances.
- An `awk` scan of lines 2440–2505 for lines beginning `>` (check 3).

**Context I did not ask for.** My runtime placed a project instruction file
(CLAUDE.md pointing at AGENTS.md) and an index of the maintainer's memory
notes in my context before I began. I did not open any file they name, and I
have not used anything in them as evidence. I note their appearance here as
the disclosure rule requires. Nothing below rests on them. I did not read
`full.diff`, hunk-03, hunk-04, `docs/`, `conformance/`, `spec/registry.json`,
git history, or the web, and I did not list the r23audit directory.

---

## 1. The passage as it now stands (spec/tarn.md 2456–2501)

Verbatim, unwrapped where I quote:

> Encoding 1 stores the document verbatim. Encoding 2 stores it as exactly one
> RFC 8878 compressed frame occupying the extent's bytes before its terminal
> CRC, **under every frame constraint `[R-COD-06]` places on a frame, named
> here or not, save two: what it states against a tile's declared decoded
> size, and what it states about the frame's declared `Window_Size`. This
> section replaces both, below. Carried over — named for convenience, not as a
> closed list — are the frame magic; no skippable frame and no second frame;
> no dictionary use, disclosed or not, and no nonzero dictionary ID; no
> content-checksum flag; and the bar on sizing any buffer from a length the
> frame itself declares.** The first exception holds because a document has no
> declared size — a reader instead decodes with a bound of its own choosing,
> no smaller than §21.9's user-metadata guarantee, and a document exceeding
> that bound is ignore-record like any other it cannot read. The frame's
> declared `Window_Size` is unconstrained here for the same reason, and takes
> the same treatment: a reader's window bound is its own, no smaller than
> §21.9's guarantee for that quantity, and a frame declaring more than the
> reader admits is ignore-record on that ground — the reader's capability, not
> a failure to decode within the meaning of R3, and no violation: the file
> exceeds a §21.9 guarantee and so remains conforming while the reader MAY
> decline it (`[R-ERR-04]`). The frame's content-size field, unlike the
> decoded size and the window, is *not* left to the reader: it MAY be present,
> and when present it MUST equal the byte length of the decoded document. **A
> mismatch is one of the frame constraints R4 registers, not a failure to
> decode under R3: the bytes decode, and what is wrong is what the header said
> about them. Routing it to R4 keeps the condition checkable from the bytes
> alone rather than turning on a decoder's tolerance (`[R-CNF-02]`)** — the
> tile rule of `[R-COD-06]` transposed to the quantity a document does have,
> its decoded length, in place of the declared size it does not. A
> **verifier** that declines to decode a document on the bound above cannot
> establish that document's conformance and MUST NOT certify the file, exactly
> as `[R-COD-11]` requires of a codec it cannot execute; ... The decline is one
> of the unchecked requirements `[R-CNF-11]` obliges the verifier to report,
> ... the verifier SHOULD report the bound it applied and the stored length of
> the extent it declined. ... Any violation here is ignore-record, never the
> tile-scope outcome §17.2 assigns. `[R-MTA-09]`

Check 3 (normative placement), run first: `awk` over 2440–2505 returns `>`
lines only at 2503–2505 (the "16 MiB figure" Note). **The whole repaired
passage is normative prose ending in `[R-MTA-09]`.** No part of either
repair sits in a blockquote. R4 is a table row in §21.5, likewise normative,
and §21.1 makes register detector/detection-point assignments do real work via
`[R-CNF-04]`. Check 3 passes for both hunks.

### The rule hunk 1 adopts, in my words

An encoding-2 user-metadata document is one zstd frame that must satisfy
**everything `[R-COD-06]` imposes on a frame** except its two decoded-size /
window statements, which §18.2 supplies afresh. Concretely, of the header's
quantities: magic pinned; skippable/second frame barred; dictionary use and
nonzero dictionary ID barred; content-checksum flag barred; trailing bytes
barred; the reader may not size a buffer from a frame-declared length; the
frame's declared `Window_Size` and the document's decoded size are *not*
constrained by the file at all but bounded by whatever the reader chooses
(floor: §21.9's 8 MiB and 16 MiB rows), with a decline on either being a
capability outcome and no violation; and the content-size field, when present,
**must equal the actual decoded byte length**, that mismatch being an R4
violation rather than an R3 decode failure.

### The rule hunk 2 adopts, in my words

Row R4 registers, as an ignore-record violation detected by a reader at extent
use, any breach of §18.2's encoding-2 frame constraints; and its instance list
now includes four content-size cases (declared-larger / declared-smaller ×
top-level / layer sub-record). The Condition cell additionally asserts that
R4's constraints bite "whether or not the bytes decode", and for content-size
"whether or not they decode to the length it declares".

---

## 2. Check 2 — every citation opened

| Citation in repaired text | Where I read it | Verdict |
|---|---|---|
| `[R-COD-06]` (line 2458, "every frame constraint … places on a frame") | 2268–2296 | **Resolves.** Full constraint inventory below. |
| `[R-COD-06]` (line 2486, "the tile rule … transposed") | 2288–2291 | **Resolves.** "The frame content-size field MAY be present; when present it MUST equal the tile's decoded size, a reader MUST treat a mismatch as a validity error at tile scope, and a reader MUST NOT allocate or size any buffer from it". §18.2's transposition changes *detectability* — see A-02/A-05. |
| §21.9 "user-metadata guarantee" | 3688 | **Resolves.** "decoded size of one user-metadata document | 16 MiB". |
| §21.9 "guarantee for that quantity" (window) | 3690 | **Resolves.** "zstd frame `Window_Size` | 8 MiB", and 3691–3702 confirms that row ranges over "the user-metadata documents and compressed frames a file actually contains" — metadata frames are in scope. |
| `[R-ERR-04]` | 3702–3715 | **Resolves.** Minimum guarantees, reader MAY decline above them, refusal reported as a resource limit. |
| `[R-CNF-02]` (line 2485) | 138–156 | **Resolves.** "File conformance is a predicate on bytes: it does not depend on any reader, writer, or environment." Supports "checkable from the bytes alone rather than turning on a decoder's tolerance". Note the *old* text used this same citation to justify the *opposite* routing (R3); the new routing is the one [R-CNF-02] actually supports, since under R3 the condition would fire or not according to whether a given zstd decoder enforces FCS. **This part of the repair is correct and is a real fix.** |
| "R4" / "R3" (§18.2, lines 2464/2474/2483) | 3545–3546 | **Resolve.** R3 = "stored bytes fail to decode"; R4 = the frame-constraint row. |
| `[R-COD-11]` (line 2451 and 2489) | 2397–2413 | **Resolves both ways.** §17.4 states the verifier-cannot-certify rule and states that software unable to execute an assigned codec is not a conforming reader. |
| `[R-CNF-10]` | 272–279 | **Resolves.** Limits live in the spec, never only in an implementation. |
| `[R-CNF-11]` | 195–223 | **Resolves**, and note it lists "when it declines to decode a user-metadata document (`[R-MTA-09]`)" *without* restricting the ground — relevant to A-07. |
| `[R-CNT-25]` / `[R-MTA-03]` / `[R-MTA-10]` (context lines) | 2422–2434, 2560–2580 | Resolve. |
| Hunk 2: `[R-MTA-09]` (R-COD-06, R-CNT-25) | as above | Resolve. |
| Hunk 2: "§18.2 states or carries over from `[R-COD-06]`" | 2456–2501 | Resolves — but see A-01/A-02 for the Condition's added clause. |

No citation in either hunk points at a rule that does not say what the citing
sentence claims. **Check 2 passes** on citation accuracy; the substantive
problems are elsewhere.

---

## 3. Check 6 / charter item 1 — every quantity the frame header can carry

RFC 8878 frame layout, and what fixes each quantity for an encoding-2
user-metadata document after the repair:

| Quantity | Fixed by |
|---|---|
| `Magic_Number` | §18.2 carried-over "the frame magic" (from `[R-COD-06]`). Registered: R4 "missing frame magic". |
| `Frame_Content_Size_flag` (presence) | §18.2: "it MAY be present". Free. |
| FCS field **width** (1/2/4/8) | **Nothing.** Encoder freedom; two files differing only here are both conforming — the class `[R-CNF-05]` licenses. Harmless. |
| `Single_Segment_flag` | **Nothing names it.** But per §17.2's own Note, setting it makes `Window_Size` *be* the frame content size — which §18.2's next sentence pins. See **A-04**. |
| `Unused_bit` | **Nothing.** RFC 8878 makes a decoder ignore it. §17.2 states the analogous encoder-freedom Note for deflate's trailing bits but not for this bit either, so this is a document-wide silence, not this repair's. Not reported. |
| `Reserved_bit` | RFC 8878 requires zero and requires a decoder to reject; reaches R3 as a decode failure. Adequately covered. |
| `Content_Checksum_flag` | §18.2 carried-over. Registered: R4 "the content-checksum flag set". |
| `Dictionary_ID_flag` / `Dictionary_ID` width | Value pinned to zero; width free. Fine. |
| `Dictionary_ID` value | §18.2 carried-over "no nonzero dictionary ID". Registered: R4. |
| Dictionary **use** with the header not disclosing it | **Newly** carried over by this repair ("no dictionary use, disclosed or not"). Undetectable, so correctly has no R4 instance — but §21.7's account of the undetectable class was not swept. See **A-06**. |
| `Window_Descriptor` / `Window_Size` | Deliberately left to the reader's own bound, floor 8 MiB. **No writer-side rule at all** — the `[R-COD-06]` SHOULD was excepted and not replaced. See **A-03**. And the "unconstrained" claim is falsified for single-segment frames. See **A-04**. |
| `Frame_Content_Size` value | §18.2: MUST equal the decoded document's byte length. Registered: R4, four new instances. |
| Block headers / block data | RFC 8878 via "exactly one RFC 8878 compressed frame"; failures reach R3. |
| `Content_Checksum` trailer | Barred via the flag. |
| Bytes after the frame, before the terminal CRC | §18.2's "occupying the extent's bytes before its terminal CRC". Registered: R4 "bytes remaining after the frame". |
| The document's actual decoded byte length | Not constrained by the file; bounded by the reader's own bound, floor 16 MiB. |

---

## 4. Charter item 3 — the carried-over / excepted partition, tested exhaustively

I first listed every constraint `[R-COD-06]` states (spec 2268–2296), then
placed each myself.

| # | `[R-COD-06]` constraint (its own words) | My placement | §18.2's placement | Agree? |
|---|---|---|---|---|
| 1 | "The stored bytes are exactly one Zstandard compressed frame as defined by RFC 8878" | carried | carried (opening sentence + "no second frame") | ✔ |
| 2 | "they MUST begin with the compressed-frame magic … a reader MUST treat a payload whose first four bytes are not that magic … as a validity error at tile scope" | carried (outcome recast) | carried, named | ✔ |
| 3 | "…or that contains a skippable frame anywhere or more than one frame, as a validity error at tile scope" | carried | carried, named | ✔ |
| 4 | "Writers MUST NOT compress **a tile** using a dictionary — whether or not the header discloses one" | carried | carried, named ("no dictionary use, disclosed or not") | ✔ — and this is a *widening* relative to the old "constraints … that do not reference a tile" test, which this clause failed. Correct as policy; §21.7 not swept (A-06). |
| 5 | "and MUST NOT emit a nonzero dictionary ID; a reader MUST treat a frame carrying a nonzero dictionary ID as a validity error at tile scope" | carried | carried, named | ✔ |
| 6 | "Writers MUST NOT set the frame's content-checksum flag … a reader MUST treat [it] as a validity error at tile scope" | carried | carried, named | ✔ |
| 7 | "and MUST NOT declare a window size exceeding the tile's decoded size" | excepted | excepted — **but it satisfies BOTH stated exceptions at once** (it is stated against a tile's declared decoded size *and* about the frame's declared `Window_Size`) | ✔ in effect, ✘ in bookkeeping — see A-03's detail |
| 8 | "The frame content-size field MAY be present; when present it MUST equal the tile's decoded size, a reader MUST treat a mismatch as a validity error at tile scope" | excepted, replaced | excepted (first exception), replaced by the decoded-length rule | ✔ |
| 9 | "and a reader MUST NOT allocate or size any buffer from **it** — the decoded size comes from the layer's declarations alone" | carried (but scoped to the FCS field) | carried, **restated broader** as "a length the frame itself declares" | ✘ — **A-05** |
| 10 | "Writers SHOULD keep the declared window within §21.9's 8 MiB `Window_Size` guarantee even for a larger tile" | excepted, needs replacing | excepted; **nothing replaces it** | ✘ — **A-03** |
| 11 | "a wider window is conforming and merely permits a conforming reader to decline the tile or the layer on resource grounds (`[R-ERR-04]`)" | excepted, replaced | replaced (ignore-record at the record, `[R-ERR-04]`) | ✔ |

So: nothing lands on **neither** side. One constraint (#7) lands on **both**
exception halves — harmless in effect, since both halves are exceptions, but
it means "save two" is not a partition of `[R-COD-06]`'s constraints; three
distinct constraints (#7, #8, #10) are excepted under two headings. And one
(#10) is excepted and then **not replaced**, contradicting the new sentence
"This section replaces both, below."

Also checked: does carrying over "every frame constraint" drag in
`[R-COD-06]`'s repeated *tile-scope outcome*? No — §18.2 closes with "Any
violation here is ignore-record, never the tile-scope outcome §17.2 assigns."
That guard is present and adequate. Similarly, "named for convenience, not as
a closed list" defuses what would otherwise be a check-5 closed-list overclaim
in the carried-over enumeration. Both of these are the repair working.

---

## 5. Charter item 2 — is the transposition faithful in modality, detectability, actor?

Side by side:

- `[R-COD-06]`: "The frame content-size field **MAY** be present; when present
  it **MUST equal the tile's decoded size**, a **reader MUST treat a mismatch
  as a validity error at tile scope**".
- §18.2: "it **MAY** be present, and when present it **MUST equal the byte
  length of the decoded document**."

**Modality:** MAY/MUST in both. Faithful.

**Actor:** `[R-COD-06]` names the reader as detector inline; §18.2 names no
actor, and supplies it only by pointing at R4 ("A mismatch is one of the frame
constraints R4 registers"), whose Detector cell reads *reader* and whose
Detected cell reads *extent use*. `[R-CNF-04]` ("A reader MUST detect every
violation the error register (§21) assigns to the reader as its detector")
makes that sufficient. Faithful, though only via the register.

**Detectability: NOT faithful.** The tile rule compares a header field to a
quantity derived from the layer's declarations — checkable with no decode at
all, which is why `[R-COD-06]` groups it with the "header-checkable" family
and why the same rule can bar the reader from allocating from it. §18.2
compares the header field to the **actual decoded byte length**, which is
knowable only *after* a complete decode. §18.2 half-acknowledges this ("the
bytes decode, and what is wrong is what the header said about them") but R4's
Condition then asserts the opposite ("broken whether or not the bytes
decode"). That divergence is **A-02**.

I note the citation "checkable from the bytes alone" is still true in the
`[R-CNF-02]` sense (the extent's bytes determine the outcome without reference
to any reader). It is *not* true in the "before decoding" sense the tile rule
enjoys, and the sentence's proximity to "transposed" invites the second
reading.

---

## 6. Check 7 — every analogy in the passage, verb against verb

1. **"whose decoder `[R-COD-11]` already requires of it for codec 3"**
   (context line, unchanged). §18.2 verb: "a conforming reader MUST be able to
   **decode** encoding 2". §17.4 verb: "software unable to **execute** an
   assigned codec or filter is not a conforming reader". Same set (a zstd
   decoder), same modality. **Passes.**

2. **"The frame's declared `Window_Size` is unconstrained here *for the same
   reason*, and takes *the same treatment*"** — the cited reason is "a document
   has no declared size". §18.2's decoded-size verb: "a document **exceeding**
   that bound"; the window verb: "a frame **declaring** more than the reader
   admits". *Exceeding an actual quantity* vs *declaring a value*: these range
   over different things — one is a fact about the decoded output, the other a
   header field. The analogy nonetheless lands where it matters (both yield
   ignore-record on the reader's capability, neither a violation), because
   `[R-COD-06]`'s window rule bounds the window *by the decoded size*, and it
   is the comparand that is missing for a document. **Passes**, with the verb
   mismatch recorded. But the "unconstrained" half fails independently — A-04.

3. **"the tile rule of `[R-COD-06]` transposed to the quantity a document does
   have, its decoded length, in place of the declared size it does not"** —
   §18.2 verb: "MUST **equal the byte length of the decoded document**";
   `[R-COD-06]` verb: "MUST **equal the tile's decoded size**". The tile's
   decoded size is "a function of the layer's declarations alone
   (`[R-SER-07]`)" per §21.9; the document's decoded length is a function of
   the bytes only after decoding. **Same modality, different epistemics.** The
   analogy is sound for the *value* constraint and unsound for the
   *detectability* it silently imports — see A-02.

4. **"exactly as `[R-COD-11]` requires of a codec it cannot execute"**
   (verifier decline). §18.2 verb: "**cannot establish** that document's
   conformance and **MUST NOT certify** the file". §17.4 verb: "**cannot
   establish** that layer's conformance and **MUST NOT certify** the file".
   Word for word identical. **Passes.**

5. **"ignore-record *like any other* it cannot read"** (decoded-size bound).
   The "others" it cannot read are §21.5's rows, every one of which "is a
   violation all the same" (§21.5 preamble). A document over the reader's own
   bound is *not* a violation — §21.5's preamble says exactly that, "except
   where a reader or verifier declines the decode on the size bound or on the
   frame's declared window". So "like any other" is an analogy on the
   *outcome* (ignore-record) that a reader could take as an analogy on the
   *status* (violation). The window clause three lines later says "and no
   violation" explicitly; the size clause does not. I looked hard at this and
   concluded it is loose rather than defective: §21.5's preamble and the §18.2
   Note both settle it, and the word "cannot read" is doing the work.
   **Passes**, recorded.

6. **"one of the frame constraints R4 registers"** — this points at a register
   row for the classification, while R4 points back at "the frame constraints
   §18.2 states". §21.1 makes the rule the source and the row the restatement;
   this pair is mutually referential. The loop closes consistently (§18.2 does
   state the FCS rule, so R4 does capture it, so §18.2's claim is true), so it
   is inelegant rather than wrong. Recorded, not reported.

7. **"the bar on sizing any buffer from a length the frame itself declares"**
   presented as *carried over*. §18.2 quantifier: "**a length the frame itself
   declares**". `[R-COD-06]` quantifier: "a reader MUST NOT allocate or size
   any buffer from **it**" — "it" being the frame content-size field alone.
   Different sets: the frame also declares `Window_Size` and every
   `Block_Size`. **Fails** — A-05.

Charter's warning realised: item 7 above is one sentence carrying the analogy
for a *list* of carried-over constraints, and it is sound for four members
(magic, frames, dictionary, checksum flag) and unsound for the fifth.

---

## 7. Check 4 — contradictions in the whole structure, including untouched text

Read: all of §18.2 (2440–2580), §21.5's preamble and all ten rows, §21.6 in
full, §21.1 in full.

- §18.2 "The frame's declared `Window_Size` **is unconstrained here**" vs
  §18.2 "when present [the content-size field] MUST equal the byte length of
  the decoded document", with §17.2's Note supplying the bridge: "with
  Single_Segment_Flag set there is no Window_Descriptor and **Window_Size is
  the frame content size**". → **A-04**, a contradiction within four lines,
  only one of them new.
- R4 Condition "the constraint is broken whether or not the bytes decode …
  whether or not they decode to the length it declares" vs §18.2 "when present
  it MUST equal the byte length of the decoded document" and vs R4's own
  Instances cell, which enumerates only *larger* and *smaller*. → **A-01**,
  **A-02**.
- §18.2 "This section replaces both, below" vs the unreplaced
  `Writers SHOULD keep the declared window within §21.9's 8 MiB Window_Size
  guarantee`. → **A-03**.
- §18.2's verifier sentence "declines to decode a document on **the bound
  above**" (singular) vs §21.5's preamble "declines the decode on the size
  bound **or on the frame's declared window**, which `[R-MTA-09]` makes that
  actor's capability". → **A-07**.
- I looked for, and did **not** find: any MUST elsewhere in §18.2 that the new
  "MAY be present" now lets an actor violate; any carve-out sentence that the
  widened carry-over collides with (the tile-scope-outcome guard at the end of
  the passage is the one that would have, and it is correct); any sentence in
  §18.1, §17.4, §19.2 or §21.6 written to be true only under the old R3
  routing (grep for "failure to decode" / "fails to decode" returns exactly
  three sites: §18.2's two and T25 — none stale).

---

## 8. Check 5 — exhaustive claims, one at a time

| Claim | Falsification attempt | Verdict |
|---|---|---|
| "**every** frame constraint `[R-COD-06]` places on a frame, named here or not" | I enumerated all eleven (§4 above). All eleven are placed. | Holds. |
| "**save two**" | Three distinct constraints are excepted (#7, #8, #10) under two headings, and #7 satisfies both headings. | **Miscounts** — folded into A-03. |
| "This section **replaces both**, below" | #10 is replaced by nothing. | **Fails** — A-03. |
| "named for convenience, **not as a closed list**" | Explicitly open. | Holds — and this is the repair correctly retiring a closed-list overclaim. |
| "The frame's declared `Window_Size` is **unconstrained** here" | Single-segment frames: Window_Size = FCS, which §18.2 pins. | **Fails** — A-04. |
| "**Both** assigned encodings are core" (context) | 1 and 2; §18.2 assigns exactly those. | Holds. |
| "§21.5 … **10 conditions**" | R1–R10 counted mechanically: 10. | Holds. |
| §21.8 "**121 conditions over 277 instances**" | Counted mechanically across §21.2–§21.5 after hunk 2: **121 / 277**, R4 = 16. | **Holds** — the four new instances are reflected. |
| §21.9 `[R-ERR-04]` "**the two** capability refusals §21.6 names" | §21.6: "Two structural cases are conforming files a reader nevertheless refuses" — foreign major, MU=1 experimental type. | Holds (not my hunk). |

---

## 9. Check 1 — tense and quantifier

Neither hunk speaks about a commit's prior versus new state; there is no
generation-sensitive quantifier in either. The quantifiers that matter are
set-quantifiers, and I checked each:

- "**every** frame constraint `[R-COD-06]` places on a frame" — ranges over
  constraints, not files. Correct set; see §4.
- "**a** document has no declared size" vs "**the** decoded document" — the
  first ranges over user-metadata documents generally, the second over the one
  this frame carries. Both correct.
- "**a** frame declaring more than the reader admits" — ranges over frames the
  file contains; matches §21.9's "compressed frames a file actually contains".
  Correct.
- R4's Condition "**A** user-metadata document stored under encoding 2" and
  Instances' two containers (top-level extent, layer sub-record extent) match
  §18.1's "A file MAY carry one user-metadata document at file scope, and each
  layer MAY carry one of its own". Correct, and consistent with every other R
  row.
- R4's "**one of** the frame constraints" — existential over constraints;
  matches. But see A-02 for the quantifier over *bytes-that-decode*.

Check 1 finds no defect of its own; the defects it feeds into are A-01 and
A-02.

---

## 10. Hunk 2, charter items — instance list derived independently first

Before reading the cell I derived the list from §18.2 plus §21.1's rules
("Where the condition compares two **magnitudes** either of which can be the
greater — a *differs from* or *does not equal* — the two directions are
likewise enumerated"; containers are an axis; §21.1's detectability gate):

1. missing frame magic × 2 containers
2. a skippable frame × 2
3. a second frame × 2
4. a nonzero dictionary ID × 2
5. content-checksum flag set × 2
6. bytes remaining after the frame × 2
7. content-size declared larger × 2
8. content-size declared smaller × 2
— undisclosed dictionary use: **no instance**, correctly, being undetectable
  (§21.1's gate, §21.7's account).
— the buffer-sizing bar: **no instance**, correctly, being a reader obligation
  that no *document* can "break".
— the window: **no instance**, correctly, §18.2 having withdrawn the
  constraint.

Total 16. The cell contains exactly these 16, in this order. **The Instances
cell matches the Condition the prose supports, no more and no fewer.** The
larger/smaller split mirrors T22, which splits the same comparison the same
way for tiles. This part of hunk 2 is right.

Which is source and which restatement: **§18.2 (`[R-MTA-09]`) is the source,
R4 the restatement.** §21.1 says so twice ("each row *restates* its governing
rule, and where a row and the rule it cites diverge, **the rule governs**"),
and R4's Governing rule cell names `[R-MTA-09]` first. Hunk 1's sentence "A
mismatch is one of the frame constraints R4 registers" partially inverts that
direction rhetorically, but does not change it.

Registered twice / by none: the only double-registration I found is R3 ∧ R4 on
a non-decoding frame carrying a content-size field, created by the row's
"whether or not the bytes decode" (A-02). §21.1's specialization list ("F1 of
F6 and of F8, F35 of F36, L24 of L25") does not include an R3/R4 pair, so
nothing arbitrates it.

---

## 11. Findings

### A-01 — R4's Condition says the content-size constraint is broken even when the field is correct

Quotation (spec 3546, R4 Condition, added text): "unlike R3, the constraint is
broken whether or not the bytes decode, **and — for the content-size field —
whether or not they decode to the length it declares**".

Read literally, "whether or not they decode to the length it declares" makes
the brokenness of the content-size constraint independent of whether the bytes
decode to the declared length — that is, present-and-correct is as much a
violation as present-and-wrong. The only condition left is *presence*, so
every encoding-2 metadata frame carrying a Frame_Content_Size field is an R4
violation, and by `[R-CNF-05]` no conforming writer may emit one.

Contradicting text, §18.2 (2478–2480): "it MAY be present, and when present it
MUST equal the byte length of the decoded document" — a correct field is
expressly permitted. And R4's own Instances cell enumerates only "declared
larger than the decoded length" and "declared smaller than the decoded
length"; there is no equal-and-still-violating instance, and §21.1 says "the
count is therefore mechanical once the cell is written".

The charitable rescue — reading the clause as being about *routing* ("it is
R4 rather than R3 whether or not they match") — makes it vacuous, since where
they match there is no condition to route. Either way the clause states
nothing usable and states one thing false.

**Repair:** delete the clause, or replace it with what the prose supports:
"…and, for the content-size field, the comparison is against the length the
bytes actually decode to, so the condition presupposes a successful decode."

**Byte-level: no.** §21.1 expressly arbitrates: "where a row and the rule it
cites diverge, **the rule governs**", and the rule here is `[R-MTA-09]`, whose
prose is unambiguous. A competent implementation applies that tiebreak, so the
emittable set does not move. I record plainly that the disputed file (an
encoding-2 metadata frame whose FCS equals the decoded length) *is* conforming
and that, absent §21.1's tiebreak, this would fork the bytes: writer X emits
it, writer Y refuses; verifier X certifies, verifier Y reports nonconforming.

### A-02 — R4 extends the content-size condition to bytes that do not decode, where §18.2 confines it to bytes that do, and where it is undecidable

Quotation (R4 Condition): "unlike R3, **the constraint is broken whether or not
the bytes decode**".

Before hunk 2 this blanket was true of every instance in the cell: magic,
skippable frame, second frame, dictionary ID, checksum flag and trailing bytes
are all header- or extent-checkable with no decode. The four new content-size
instances are not. If the bytes do not decode, there is no decoded length, and
"declared larger/smaller than the decoded length" names nothing.

Contradicting text, §18.2 (2480–2482): "A mismatch is one of the frame
constraints R4 registers, not a failure to decode under R3: **the bytes
decode**, and what is wrong is what the header said about them." The governing
rule conditions the whole classification on a successful decode; the row
asserts the opposite for the same instances.

Two concrete consequences. (i) A frame that carries FCS = 100 and dies at byte
50 of the decode is registered by R3 (bytes fail to decode) *and* by R4 (the
row says the constraint bites anyway) — §21.1's specialization list does not
contain this pair, so nothing says which row the file is recorded against, and
a corpus built per §21.8 ("one vector per instance") cannot say which expected
outcome a vector carries. (ii) It hides the one respect in which hunk 1's
transposition is unfaithful: `[R-COD-06]`'s tile version compares the field to
a size derived from the layer's declarations and is checkable before any
decode, while §18.2's version compares it to the actual decoded length and is
not. The row papers over exactly that difference.

**Repair:** confine the blanket to the header constraints it was written for —
e.g. "unlike R3, a header constraint is broken whether or not the bytes decode;
the content-size condition instead presupposes a decode and compares the
field to the length produced."

**Byte-level: no.** Both R3 and R4 carry the identical outcome (ignore-record),
detector (reader) and detection point (extent use), so no reader's accept/
reject behaviour turns on the routing, and §21.1's tiebreak resolves the
divergence in favour of §18.2. What moves is the conformance corpus's
instance accounting, not bytes on disk.

### A-03 — "This section replaces both" is false: the writer-side window SHOULD is excepted and replaced by nothing

Quotation (§18.2, 2458–2462): "save two: what it states against a tile's
declared decoded size, and **what it states about the frame's declared
`Window_Size`. This section replaces both, below.**"

`[R-COD-06]` states three things about the declared window: the MUST NOT
exceeding the tile's decoded size; "**Writers SHOULD keep the declared window
within §21.9's 8 MiB `Window_Size` guarantee even for a larger tile**"; and
that a wider window is conforming and merely permits a decline. §18.2 replaces
the first (withdrawn) and the third (recast as ignore-record at the record). It
replaces the second with nothing, and its own window sentences are entirely
reader-side: "a reader's window bound is its own… a frame declaring more than
the reader admits is ignore-record".

Why it bites. §21.9's `Window_Size` row is 8 MiB and, by the paragraph beneath
the table, ranges over "the user-metadata documents and compressed frames a
file **actually contains**" — metadata frames included. §21.9's `[R-ERR-03]`
tells writers "a writer MAY rely on that" about the 16 MiB user-metadata
guarantee. After the repair, a writer may emit a 12 MiB metadata document in a
frame declaring a 64 MiB window, entirely conforming, and every conforming
reader may lawfully ignore-record it — and no rule anywhere, not even a
SHOULD, steers the writer away. On the tile path the identical trap is closed
by the SHOULD this repair excepted away. The repair thus left the guarantee it
leans on ("no smaller than §21.9's guarantee for that quantity") silently
defeatable from the writer side.

Also in this sentence: "save **two**" is not a partition. `[R-COD-06]`'s
"MUST NOT declare a window size exceeding the tile's decoded size" satisfies
*both* named exceptions at once — it is stated against a tile's declared
decoded size and it is about the frame's declared `Window_Size` — so two
headings cover three constraints and one constraint lands on both. Harmless in
effect (both headings are exceptions) but it is why the missing third one was
easy to lose.

**Repair:** add the writer guidance §18.2 dropped, e.g. "Writers SHOULD keep a
document frame's declared window within §21.9's 8 MiB `Window_Size`
guarantee"; and either say "save what it states against a tile's declared
decoded size and what it states about the frame's declared `Window_Size`"
without the count, or say "save three".

**Byte-level: no.** A SHOULD is advisory: `[R-CNF-12]` says "§21's register
enumerates MUST-level conditions only" and a SHOULD deviation "does not bar
certification". Adding it changes which files a writer is *advised* to emit,
not which it *may* emit, and no reader's verdict changes.

### A-04 — "the frame's declared Window_Size is unconstrained here" is false for a single-segment frame, whose window the very next sentence pins

Quotation (§18.2, 2470–2472): "**The frame's declared `Window_Size` is
unconstrained here** for the same reason, and takes the same treatment…"

§17.2's Note states the mechanism in the document's own words: "with
Single_Segment_Flag set there is no Window_Descriptor and **Window_Size is the
frame content size**". §18.2's next sentence says the content-size field, "when
present it MUST equal the byte length of the decoded document". So in any
metadata frame with Single_Segment_flag set — and RFC 8878 requires the
content-size field to be present in exactly that case — the declared window is
pinned, to the decoded document's byte length, by §18.2 itself.

§17.2 works this interaction out for tiles in a dedicated Note and closes it
("no conforming file turns on which derivation a reader implements"). §18.2
carries the analogy across but not the Note, and states the flat "unconstrained"
that the Note exists to qualify. A reader taking "unconstrained" at face value
concludes it may never treat the window as constrained; a reader that computes
Window_Size the single-segment way sees it pinned.

**Repair:** qualify — "The frame's declared `Window_Size` is unconstrained
here save as the content-size rule below pins it in a single-segment frame,
where RFC 8878 derives the window from that field (§17.2)."

**Byte-level: no.** Both readings permit the same files: a single-segment frame
whose FCS equals the decoded length satisfies the content-size MUST under
either, and the reader's window bound is a MAY under either. Nothing a writer
may emit and no accept/reject verdict moves.

### A-05 — the carried-over buffer bar is restated broader than the rule it carries over from

Quotation (§18.2, 2464–2466): "and **the bar on sizing any buffer from a
length the frame itself declares**."

`[R-COD-06]` (2288–2291): "The frame content-size field MAY be present; when
present it MUST equal the tile's decoded size, a reader MUST treat a mismatch
as a validity error at tile scope, and **a reader MUST NOT allocate or size any
buffer from it** — the decoded size comes from the layer's declarations alone".
"It" is the content-size field, and one field only.

A zstd frame declares more than one length: `Window_Size` and every
`Block_Size`. §18.2's restatement covers all of them. That is not a harmless
generalisation here, because §18.2 has just *removed* the window constraint and
made the reader compare the frame's declared window against its own bound —
a reader that checks `Window_Size` ≤ 8 MiB and then allocates a window of that
size is doing the obvious thing, and the broadened bar forbids it, leaving
"allocate your full bound unconditionally" as the only compliant behaviour. The
sentence presents this as *carried over*, so nothing signals that a rule has
been widened.

If the widening is wanted — and §17.2's Note "a reader allocates from
declarations, never from stored data or embedded size fields" suggests the
document's instinct is that direction — it should be stated as §18.2's own new
rule, not smuggled in under "carried over".

**Repair:** either narrow to the source ("the bar on sizing any buffer from
the frame's content-size field") or state it as new and say what a reader
*does* size its window from.

**Byte-level: no.** It constrains a reader's internal allocation only. No file
becomes emittable or unemittable, and no accept/reject verdict changes.

### A-06 — §21.7's account of the undetectable class was not swept when §18.2 took on undisclosed dictionary use

Quotation (§18.2, 2463–2464): "no **dictionary use, disclosed or not**, and no
nonzero dictionary ID".

This is new. Under the wording it replaced — "the frame constraints of
`[R-COD-06]` that do not reference a tile", followed by a closed list of four
— `[R-COD-06]`'s "Writers MUST NOT compress **a tile** using a dictionary —
whether or not the header discloses one" referenced a tile and was not in the
closed list, so it did not carry. It carries now, which creates a new class of
violation: a writer that compresses a *user-metadata document* against an
undisclosed dictionary. `[R-COD-06]` says of the tile version that it "is not
detectable by inspection and need not decode to an error: it is a writer
violation whose consequence is wrong decoded content".

§21.1 makes the disposal of undetectable violations explicit: register
completeness runs to *detectable* violations, "detectability being the gate
`[R-CNF-07]` already applies and **§21.7 the account, by class, of what fails
it**". §21.7's account reads: "A writer that emits well-formed structures
carrying **wrong sample values** — a mis-strided filter (`[R-COD-10]`), **an
undisclosed compression dictionary (`[R-COD-06]`)**, or simply wrong data".
A user-metadata document is not a sample value; §18.1 calls it application
data and `[R-MTA-02]` bars it from affecting any byte's decoding. So the newly
created class falls into neither §21.5 (correctly — undetectable) nor §21.7's
account as written.

**Repair:** extend §21.7's sentence to cover the document case — e.g. widen
"wrong sample values" to "wrong sample values, or a wrong user-metadata
document", and cite `[R-MTA-09]` alongside `[R-COD-06]` on the dictionary item.

**Byte-level: no** for the §21.7 gap itself, which is descriptive. I note
separately that the underlying widening in §18.2 *is* byte-level and is
presumably intended: it newly bars a conforming writer from emitting a
dictionary-compressed metadata frame that the old closed list permitted.

### A-07 — the verifier consequence is supplied for one of the passage's two reader bounds

Quotation (§18.2, 2487–2496): "A **verifier** that declines to decode a
document on **the bound above** cannot establish that document's conformance
and MUST NOT certify the file… the verifier SHOULD report **the bound it
applied** and the stored length of the extent it declined."

The passage now creates two reader-side bounds — a decode-size bound and a
window bound — and the verifier sentence's singular "the bound above" names
one. §21.5's preamble restates `[R-MTA-09]` as covering both: "except where a
reader or verifier declines the decode **on the size bound or on the frame's
declared window**, which `[R-MTA-09]` makes that actor's capability and not a
fact about the file". Under §21.1 the rule governs the restatement, and the
rule as written does not say that a verifier declining on the window may not
certify. A verifier reading strictly could certify a file whose metadata
document it never decoded and whose R5–R10 content rules therefore went
unchecked.

The hole is closed in practice by `[R-CNF-11]`, which lists "when it declines
to decode a user-metadata document (`[R-MTA-09]`)" as a cannot-establish
ground without qualifying the ground. So this is an ambiguity, not a licence.
It is worth fixing because hunk 1's new "This section replaces both, below"
advertises §18.2 as supplying complete replacements for both excepted
constraints, and the verifier consequence is where the replacement stops
short.

**Repair:** make it plural and explicit — "A verifier that declines to decode
a document on either bound above…" and "the bound it applied and which
quantity it bounded".

**Byte-level: no.** `[R-CNF-11]` independently imposes the cannot-establish
obligation for any decline to decode a user-metadata document, so both
readings converge on the same verdict.

---

## 12. What passed

- **Check 1** (tense/quantifier): no generation-sensitive quantifier in either
  hunk; every set-quantifier I checked matches its source (§9).
- **Check 2** (citations): every identifier and section number in both hunks
  opened and verified; all twelve resolve as claimed (§2).
- **Check 3** (normative placement): the entire §18.2 repair is plain prose
  under `[R-MTA-09]`, with the only `>` lines in the range at 2503–2505; R4 is
  a register row. Neither repair is stranded in a blockquote, and no
  blockquote elsewhere still asserts the pre-repair R3 routing (grep for
  "failure to decode"/"fails to decode" returns three sites, all current).
- **Check 5** (exhaustive claims): §21.8's "121 conditions over 277 instances"
  and §21.5's "10 conditions" both verified mechanically against the current
  tables, R4's four new instances included; "not as a closed list" correctly
  retires the old closed-list overclaim. The failures are A-03 and A-04.
- **Hunk 2's Instances cell**: derived independently before reading, matches
  exactly, 16 for 16, and its larger/smaller split is what §21.1's magnitude
  rule requires and what T22 already does for tiles.
- **The core of hunk 1's repair — rerouting the content-size mismatch from R3
  to R4 — is correct**, and fixes a real inconsistency: T22 and T25 already
  keep FCS mismatch separate from decode failure for tiles, and `[R-CNF-02]`
  genuinely supports R4 (under R3 the condition would fire or not according to
  a given decoder's FCS tolerance). The problems are in what the repair
  carried alongside it and in how the row restates it.
