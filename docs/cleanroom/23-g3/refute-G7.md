# Refute-only pass, group G7 — window governance (X-04, A-04, A-07)

## 0. Disclosure

Read, in this order:
- `/private/tmp/.../r23audit/refute/finding-X-04.md`
- `/private/tmp/.../r23audit/refute/finding-A-04.md`
- `/private/tmp/.../r23audit/refute/finding-A-07.md`
- `/private/tmp/.../r23audit/hunk-01.diff`
- `/private/tmp/.../r23audit/hunk-04.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — regions
  95–300, 2260–2320, 2440–2520, 3520–3560, 3655–3745, and §21.1 in full.

Ran only `sed`/`awk`/`grep` against `spec/tarn.md`. Did not read `docs/`,
`conformance/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
`spec/registry.json`, `full.diff`, hunks 2 or 3, or any git history. Did not
list the audit directory. No web access.

**Unrequested context appeared before I began.** The runtime placed in my
context: a project instruction file pointer, an index of the maintainer's
memory notes with descriptive titles, and a git status block listing five
recent commit subject lines. Two of those subject lines name the very
subsections and mechanisms under audit (§18.2's carry-over, §21.9's tile-row
quantification, and an R4 routing decision). I did not open any of the files
they name and I have not used any of them as evidence; every conclusion below
is sourced to a line of `spec/tarn.md` that I quote. But their presence is a
disclosed breach of the blindness the access rule intends, and it is recorded
here rather than left silent. In particular, the commit subjects would have
told me what the repairs were *intended* to do — which is exactly the framing
contamination this audit exists to avoid — so I deliberately reconstructed
each repair's effect from the diff and the surrounding prose instead.

---

## 1. The passage, enumerated

§18.2, lines 2456–2501 (post-repair, as it stands now):

```
2456 Encoding 1 stores the document verbatim. Encoding 2 stores it as
2457 exactly one RFC 8878 compressed frame occupying the extent's bytes
2458 before its terminal CRC, under every frame constraint `[R-COD-06]`
2459 places on a frame, named here or not, save two: what it states
2460 against a tile's declared decoded size, and what it states about
2461 the frame's declared `Window_Size`. This section replaces both,
2462 below. Carried over — named for convenience, not as a closed list —
2463 are the frame magic; no skippable frame and no second frame; no
2464 dictionary use, disclosed or not, and no nonzero dictionary ID; no
2465 content-checksum flag; and the bar on sizing any buffer from a
2466 length the frame itself declares. The first exception holds because
2467 a document has no declared size — a reader instead decodes with a
2468 bound of its own choosing, no smaller than §21.9's user-metadata
2469 guarantee, and a document exceeding that bound is ignore-record
2470 like any other it cannot read. The frame's declared `Window_Size`
2471 is unconstrained here for the same reason, and takes the same
2472 treatment: a reader's window bound is its own, no smaller than
2473 §21.9's guarantee for that quantity, and a frame declaring more
2474 than the reader admits is ignore-record on that ground — the
2475 reader's capability, not a failure to decode within the meaning of
2476 R3, and no violation: the file exceeds a §21.9 guarantee and so
2477 remains conforming while the reader MAY decline it (`[R-ERR-04]`).
2478 The frame's content-size field, unlike the decoded size and the
2479 window, is *not* left to the reader: it MAY be present, and when
2480 present it MUST equal the byte length of
2481 the decoded document. ...
```

What §18.2 says about the **window**, exhaustively:

| # | Statement | Line | Force |
|---|---|---|---|
| W1 | [R-COD-06]'s window statements are excepted from the carry-over | 2459–2461 | normative (an exclusion) |
| W2 | "This section replaces both, below" | 2461–2462 | normative (a promise) |
| W3 | "The frame's declared `Window_Size` is unconstrained here" | 2470–2471 | normative |
| W4 | reader's window bound is its own, floor = §21.9's guarantee | 2472–2473 | normative |
| W5 | a frame declaring more than the reader admits → ignore-record, reader capability, no violation | 2473–2476 | normative |
| W6 | such a file "exceeds a §21.9 guarantee and so remains conforming while the reader MAY decline it" | 2476–2477 | normative |

Nothing else in §18.2 is about the window. There is **no writer-side
statement about the window at all.**

Every other sentence in the document that constrains a zstd frame's window
(exhaustive, from `grep -n "Window_Size\|window"`):

- 2285–2287 — [R-COD-06]: "MUST NOT declare a window size exceeding the
  tile's decoded size; a reader MUST treat either as a validity error at
  tile scope". Tile-scoped.
- 2292–2296 — [R-COD-06]: "Writers SHOULD keep the declared window within
  §21.9's 8 MiB `Window_Size` guarantee even for a larger tile; a wider
  window is conforming and merely permits a conforming reader to decline the
  tile or the layer on resource grounds (`[R-ERR-04]`)." Tile-scoped.
- 2298–2306 — §17.2 Note, blockquote, the *only* place in the document that
  states the single-segment derivation. Self-scopes: "for a **tile** this
  rule they agree".
- 3513 — §21.4 row T21: "Codec 3 (zstd) and the frame declares a window size
  larger than the tile's decoded size … tile use … `[R-COD-06]`".
  Tile-scoped.
- 3529–3532 — §21.5 preamble carve-out for a decline "on the size bound or
  on the frame's declared window".
- 3690 — §21.9 row: `| zstd frame Window_Size | 8 MiB |`.
- 3729 — §21.9 Note on where 8 MiB comes from.
- 4100 — Appendix summary table, restating §21.9.

Greps run and their output:

```
$ grep -n "Single_Segment\|single-segment\|single segment" spec/tarn.md
2299:> tile this rule they agree: with Single_Segment_Flag set there is no
2305:> only as a single-segment frame, and no conforming file turns on which

$ grep -n "8 MiB" spec/tarn.md
2293:declared window within §21.9's 8 MiB `Window_Size` guarantee even
3690:| zstd frame `Window_Size` | 8 MiB |
3729:> ordinary, so the guarantee never binds a typical file; 8 MiB is
4100:| Reader minimum guarantees | ... 8 MiB zstd window | §21.9 |
```

Two facts fall straight out, and both are in the auditors' favour:

1. **`Single_Segment` occurs exactly twice in the whole document, both inside
   one blockquote, and that blockquote's first clause scopes it to tiles.**
   By [R-CNF-01] (lines 104–106) it carries no normative force. So a reader
   of the normative text alone is never told, anywhere, that a frame with no
   Window_Descriptor still has a `Window_Size`.
2. **The only "8 MiB" writer guidance in the document is at line 2293 and is
   scoped to tiles.** §18.2 has no counterpart, and W1 expressly excepts
   line 2293's sentence — it is unambiguously "what [R-COD-06] states about
   the frame's declared `Window_Size`". W2 promises a replacement for it.
   None is supplied.

So X-04's mechanical claim is **correct as stated**: the repair excepted a
writer SHOULD and did not replace it, while its promise at 2461–2462 says it
did. A-04's mechanical claim is also correct: for a single-segment frame the
window is the content-size field, which line 2480 pins.

The remaining question is the only one I was asked: does any of it move
bytes.

---

## 2. Constructions built

### C1 — the 12 MiB single-segment metadata document (X-04's own file)

File S: conforming TARN file, top-level user-metadata record, encoding 2,
one zstd frame with Single_Segment_Flag set, Frame_Content_Size = 12 MiB
(RFC 8878 requires FCS present in that case), document decodes to 12 MiB.
By RFC 8878, Window_Size = FCS = 12 MiB.

- 12 MiB ≤ 16 MiB, the §21.9 user-metadata row: within.
- 12 MiB > 8 MiB, the §21.9 `Window_Size` row: **exceeds.**
- Hunk 4's rewritten paragraph (3691–3703) confirms the window row ranges
  over "compressed frames a file actually contains" — a metadata frame is
  one. §18.2 line 2476 independently confirms it: a wide-window metadata
  frame means "the file exceeds a §21.9 guarantee".

Consequence: [R-CNF-03]'s acceptance duty (lines 158–167: "and none of whose
values exceeds the minimum guarantees of §21's limits table") **lapses**, and
§21.9's [R-ERR-04] paragraph (3705–3707) lets a conforming reader decline the
whole file. A writer that relied on §21.9's 16 MiB document guarantee — which
[R-ERR-03] at 3678–3680 expressly invites: "a writer MAY rely on that" — has
silently forfeited it by choosing single-segment framing, and the document
never told it so.

**Does the emittable set move?** File S is conforming under both readings.
§21.9 line 3705: "A file exceeding any of these remains conforming". No
register row fires: T21 (3513) is tile-scoped; R4's instance list (3546) has
sixteen instances and **no window instance**; §21.5's preamble (3529–3532)
carves the window decline out of the violation set. And the rule X-04 wants
added is a SHOULD, which [R-CNF-12] settles at lines 260–262: "Deviation from
a SHOULD is not a violation for this purpose … a verifier reports a SHOULD
deviation as an advisory that does not bar certification." [R-COD-06] itself
says of the tile analogue, line 2294, "a wider window is conforming". So
adding the missing sentence removes no file from the conforming set, and
[R-CNF-05] bars nothing extra. **The set does not move.**

**Does any accept/reject verdict move?** Only if two implementations reading
this document could disagree on the *value* of File S's Window_Size. See C2.

### C2 — the "a single-segment frame has no Window_Size" reader

This is the sharpest available attack, and it is the one the A-04 verifier
half-conceded when it wrote that the subject "the frame's **declared**
`Window_Size` … does not even denote in that case."

Implementation A reasons: §18.2 speaks only of a "declared" `Window_Size`;
a single-segment frame declares none (no Window_Descriptor); the document's
only account of the derivation is a non-normative Note scoped to tiles;
therefore File S exceeds no §21.9 row; therefore by [R-CNF-03] I MUST accept
it, and any reader that declines it on that ground "is not a conforming
reader" (§21.9, line 3708–3709).

Implementation B reasons: Window_Size = 12 MiB; the row is exceeded; I MAY
decline the file entirely.

If A's reading were available, this is a live fork: the same byte sequence is
MUST-accept for A and MAY-decline for B, and each calls the other
nonconforming. That is squarely an accept/reject fork.

**It is not available.** Line 2457 incorporates RFC 8878 normatively: the
stored bytes are "exactly one RFC 8878 compressed frame" (and line 2269–2271
for tiles: "as defined by RFC 8878"). A reader must consult RFC 8878 to parse
the frame header at all, and RFC 8878 defines `Window_Size` for every frame,
including the single-segment case where it equals `Frame_Content_Size`.
§21.9's row names the RFC quantity — "zstd frame `Window_Size`" — not "the
declared window", so its subject exists whenever the frame does. And §18.2's
own line 2476 tells the reader that a metadata frame *can* put the file over a
§21.9 guarantee on window, which A's reading would make impossible. A's
reading requires ignoring an incorporated normative reference and
contradicting line 2476. It is a misreading, not a second reading.

So both implementations compute 12 MiB, both find the row exceeded, both have
the same lapsed duty and the same MAY. **No verdict moves.** (Note the shape
of this answer: it establishes that the two implementations reach the same
bytes and the same verdict — not merely that the auditor was imprecise. That
is the distinction the charter asks for, and it is met here.)

### C3 — the narrow-exception reading (does exception (b) swallow the SHOULD?)

Reading 1: exception (b) at 2460–2461, "what it states about the frame's
declared `Window_Size`", covers *all* of [R-COD-06]'s window statements,
including the writer SHOULD at 2292–2296. The SHOULD is gone, unreplaced.
(X-04's reading. I agree it is the natural one.)

Reading 2: exception (b) covers only [R-COD-06]'s *constraint* on the window
(the MUST NOT at 2285–2286), and the SHOULD survives via the broad carry-over
"every frame constraint `[R-COD-06]` places on a frame, named here or not"
(2458–2459), transposed to "even for a larger document".

Do these fork bytes? No. The disputed item is a SHOULD in both readings, and
[R-CNF-12] lines 260–262 remove SHOULD deviation from the violation set
entirely, while [R-COD-06] line 2294 confirms the wide window "is
conforming". A verifier reports a SHOULD deviation "as an advisory that does
not bar certification" (261–262) and "owes no search for one" (263). So the
two readings differ only in whether an advisory line may appear in a report.
Not a byte, not a verdict. **Set does not move.**

### C4 — did the repair widen the carry-over enough to *re-import* a tile rule?

The repair replaced the old filter "the frame constraints of `[R-COD-06]`
**that do not reference a tile**" (hunk 1, `-` side) with "every frame
constraint `[R-COD-06]` places on a frame, named here or not, **save two**".
That is a genuine widening: tile-referencing constraints are no longer
filtered out by their own wording; only the two named exceptions escape.

I tried to build a file where the widening re-imports [R-COD-06]'s window
MUST NOT (2285–2286) against a document. It cannot: that sentence is covered
by *both* named exceptions — it is stated against "the tile's decoded size"
(exception (a)) and it is a statement about the declared window (exception
(b)) — and line 2470–2471 flatly says the window "is unconstrained here". A
reader cannot apply a MUST NOT the same paragraph disclaims four lines later.

I also checked the small-document case, since [R-COD-06]'s Note (2302) says
the Window_Descriptor cannot express less than 1 KiB. A 20-byte metadata
document framed with a Window_Descriptor declares ≥ 1 KiB of window, which
for a *tile* would violate 2285–2286. Exception (b) is exactly what frees a
document from that, and 1 KiB ≤ 8 MiB so no §21.9 row is touched. The
exception is byte-neutral and well-motivated here. **No construction.**

### C5 — the content-size pin as a hidden window pin (A-04's core)

A-04 is right that in a single-segment frame the window is fully determined
by the field line 2480 pins. But determination is not conflict: line 2480
requires FCS = decoded length, and RFC 8878 makes Window_Size = FCS, so the
derived window is the decoded length. There is no choice a writer had that
this takes away, and nothing a reader could compute two ways. §17.2's Note
says the same for tiles: the requirement "already obliges" the derived value
to be right, and "no conforming file turns on which derivation a reader
implements" (2305–2306). The disputed file class is empty. **No
construction.**

### C6 — the R4 routing (hunk 1's other change) against the window

Hunk 1 re-routed a content-size mismatch from R3 to R4 (lines 2481–2485).
I checked whether that leaves a §18.2 frame constraint registered by R4 with
no instance, which would be a §21.1 completeness defect ("Its **completeness
is normative**"). Walking §18.2's carry-over list at 2462–2466 against R4's
instances at 3546:

| §18.2 carry-over | R4 instance? |
|---|---|
| frame magic | yes (×2 extents) |
| no skippable frame | yes |
| no second frame | yes |
| no nonzero dictionary ID | yes |
| no dictionary use, undisclosed | no — [R-COD-06] 2280–2283 says it is undetectable, so §21.1's gate ("detectable") excludes it |
| no content-checksum flag | yes |
| bar on sizing a buffer from a declared length | no — a reader duty, not a file property |
| single frame occupying the extent | yes ("bytes remaining after the frame") |
| content-size field pinned | yes, both directions |
| **window** | **excepted, so nothing to register** |

Consistent. Sixteen instances, no gap, and no window instance is owed because
no window constraint is in force. **No construction.**

### C7 — A-07: the verifier and the second bound

Question: can a verifier that declines to decode a metadata document *on the
window bound* certify the file?

Two readings of "the bound above" (2488): (i) both bounds; (ii) the decode-
size bound only.

Under (i), 2487–2488 bars certification outright. Under (ii), §18.2 is silent
— but [R-CNF-11] is not. Lines 202–203 list as a cannot-establish ground
"when it declines to decode a user-metadata document (`[R-MTA-09]`)",
**unqualified as to ground**, and lines 207–208: "a verifier MUST NOT certify
a file it reports that way." And §21.5's preamble at 3529–3532 names the
window decline as exactly an [R-MTA-09] decline: "where a reader or verifier
declines the decode on the size bound **or on the frame's declared window**,
which `[R-MTA-09]` makes that actor's capability". So a window decline is
inside [R-CNF-11]'s ground by the document's own naming.

I looked for the escape: a verifier arguing it declined *the frame* rather
than *the document*, so [R-CNF-11]'s ground never attaches. 3529–3532
forecloses it by naming the window decline as a decline of "the decode" under
[R-MTA-09], the user-metadata document rule. And §18.2's own sentence at
2492–2494 imports rather than narrows the scope: "The decline is one of the
unchecked requirements `[R-CNF-11]` obliges the verifier to report."

I also checked whether the drafters ever exclude a ground when they mean to —
they do, at 2497–2500 for an unassigned encoding ("leaves no document rule
attached and is `[R-MTA-10]`'s subject, not a decline") and at 203–206. No
such exclusion exists for the window decline.

Both readings converge on: cannot establish, MUST NOT certify. **No verdict
forks. No construction.**

### C8 — the single-segment gap read as an R3 mis-route

Last attempt. Line 2475–2476 says a window decline is "not a failure to
decode within the meaning of R3" — but that clause is predicated on "a frame
**declaring** more than the reader admits" (2473). If "declaring" excludes
the single-segment case, a strict reader declining File S on window is
outside the carve-out, and §21.5's preamble ("every way its document can be
unreadable takes this outcome … as a violation in the rows below") would push
it into R3 — a *violation*, reported as a validity error rather than a
resource limit, which [R-ERR-04] at 3712–3714 forbids ("a refusal on resource
grounds MUST be reported as a resource limit and not as a validity error").
That would be a verifier-verdict fork: *nonconforming* versus *cannot
establish*.

It fails on two independent grounds. First, R3's condition is that the stored
bytes "**fail to decode**" (3545); a reader that declined has established
nothing about whether they decode, and [R-CNF-04] line 176–178 bars it from
inferring — "A reader MUST NOT heuristically repair a violating structure or
infer values this specification does not define." A decline is not a failure.
Second, the document's own usage of "declare" already covers the derived
case: [R-COD-06] line 2285 says "MUST NOT **declare** a window size", and its
Note reconciles the single-segment derivation with that very verb, treating
the derived value as the declared one. §18.2's "declaring" inherits that
usage. **No construction.**

---

## 3. Result

All three findings: the downgrade stands on byte-level. None of X-04, A-04,
A-07 moves the emittable set or any accept/reject or certify verdict.

But X-04 is **not fully answered by the document**, and that is worth
separating from the byte-level grade. Its mechanical claim survives intact:

- §18.2 line 2461 promises "This section replaces both, below."
- Exception (b) removes [R-COD-06]'s writer SHOULD at 2292–2296.
- §18.2 supplies **no** writer-side window statement at all.
- The single-segment derivation, which makes the promise consequential
  above 8 MiB, appears **only** in a non-normative Note that scopes itself
  to tiles (2298–2306) — [R-CNF-01], lines 104–106.
- The result is that §21.9's 16 MiB user-metadata guarantee, which
  [R-ERR-03] line 3680 invites a writer to rely on, is not in fact available
  above 8 MiB to a writer that chooses single-segment framing, and no
  normative sentence anywhere warns it.

That the arithmetic works out byte-neutral is a property of SHOULD, not of
the passage being complete. The reasoning that makes it byte-neutral is
nowhere in the document either; a reader has to derive it from [R-CNF-12]
and RFC 8878 unaided. The missing sentence is recorded in the structured
result.
