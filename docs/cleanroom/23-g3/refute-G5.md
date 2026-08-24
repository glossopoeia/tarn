# Refute-only pass, group G5 (finding X-03)

## What I read / ran

Read in full:
- /private/.../r23audit/refute/finding-X-03.md
- /private/.../r23audit/hunk-01.diff (§18.2, lands ~2448)
- /private/.../r23audit/hunk-02.diff (§21.5 R4 row, lands ~3536)

Spec passages opened (spec/tarn.md), by sed range:
- 2440-2520 (§18.2 encoding-2 passage incl. the flagged sentence and the Note)
- 2270-2300 (§17.2 [R-COD-06])
- 120-230 (§2.3 conformance classes: R-CNF-02..R-CNF-11)
- 2395-2415 (§17.4 [R-COD-11]); 2555-2580 (§18.2 [R-MTA-05], [R-MTA-10])
- 3295-3330 (§21.1), 3370-3385 (§21.2 preamble), 3600-3660 (§21.7)
- 3528-3540 (§21.5 preamble), 2478-2490 numbered, 3689 (§21.9 row)

Greps run: a whitespace-normalised python scan of the whole file (defeats the
hard wrap) for "bytes alone", "header-checkable", "checkable", "from the
bytes"; plus line greps for R-CNF-*, R-RDR-02, and the §21.9 user-metadata row.

Contamination disclosure: my runtime injected a CLAUDE.md pointer and an index
of the maintainer's private memory files (titles only, including one naming an
ADR number and one naming §18.2's carry-over). None of it is specification
text. I did not open any of those files and did not use their contents; I flag
it because a title in that index touches the same subsection.

## The normalised grep, verbatim output

=== "bytes alone"
1329 | ...one whose stored bytes alone fail its crc keeps its extent...
2484 | ...Routing it to R4 keeps the condition checkable from the bytes alone rather than turning on a decoder's tolerance (`[R-CNF-02]`)...

=== "header-checkable"
2287 | ...a reader MUST treat either as a validity error at tile scope, both being header-checkable. The frame content-size field MAY be present...

=== "checkable"
2251 | ...a reader MUST treat a mismatch as a validity error at tile scope — checkable from the entry and the layer record alone, before any payload fetch. `[R-COD-04]`
2287 | (above)
2325 | ...a reader MUST treat such a declaration as a validity error at layer scope, checkable from declarations alone. `[R-COD-07]`
2484 | (above)

## Step-by-step: what a checker must do

Condition: "content-size field, when present, equals the byte length of the
decoded document."
1. Locate the extent, strip the terminal CRC-32C ([R-CNT-20]).
2. Parse the zstd frame header; read Frame_Content_Size if the descriptor says
   it is present.
3. Decode the frame to end-of-frame. The reader MUST NOT size a buffer from a
   length the frame declares — hunk 1 carries that bar over explicitly
   ("the bar on sizing any buffer from a length the frame itself declares",
   2464-2465). So the decode runs against the reader's own bound.
4. Count the produced bytes; compare.

So: a full decode is required. The auditor is factually right about step 3-4.
The question is whether the sentence claims otherwise, and whether anything
byte-visible turns on it.

## Attacking the downgrade's premise

The downgrade rests on one claim: "checkable from the bytes alone" asserts
decoder-independence, not header-only inspection. I tried to break it.

Attack 1 — lexical idiom. The document's other "checkable from X alone"
constructions do name a *proper subset* of the file and do assert locality:
2251 "checkable from the entry and the layer record alone, before any payload
fetch"; 2325 "checkable from declarations alone"; 2287 "header-checkable".
That is a real idiom and it is the auditor's best card. But it breaks on the
parameter: at 2251 and 2325 the excluded thing is the payload; at 2484 the
parameter is "the bytes", the maximal set, which excludes nothing inside the
file. The only thing "the bytes alone" can exclude is something outside the
file — and the sentence names it in the same clause: "rather than turning on a
decoder's tolerance". Attack fails.

Attack 2 — does the transposition sentence contradict itself ("two halves
point opposite ways")? No. The second half names the comparand outright —
"the quantity a document does have, its decoded length, in place of the
declared size it does not" — which is an explicit statement that the comparand
is NOT a declaration and must be obtained by decoding. A reader who took half
one as header-only would be contradicted by half two of the same sentence and
by the R4 row's instances ("declared larger/smaller than the decoded length",
3546). Attack fails.

Attack 3 — is the claim even TRUE of the new routing? I expected this to be
the auditor's kill shot and it runs the other way. Under the old R3 routing
the condition was "the stored bytes fail to decode", which for a real RFC 8878
decoder is exactly decoder-dependent: zstd errors on a content-size mismatch,
a tolerant decoder need not. The repair moves the condition to "content-size
field ≠ decoded length", a deterministic function of the byte string, and
[R-CNF-02] ("a pure predicate on bytes: it does not depend on any reader,
writer, or environment", 138-139) is the right citation for exactly that.
The clause is more accurate after the repair than before it. Attack fails.

Attack 4 — is any normative duty keyed on checkability? Searched for one.
§21.1's completeness gate is *detectability* ("detectability being the gate
`[R-CNF-07]` already applies", 3312), and §21.7 defines the undetectable class
by absence of a file-level witness ("no file-level witness exists to check",
3621), never by whether a decode is needed. §21.5 rows R5-R10 all test the
decoded document and all carry detector "reader", detection point "extent
use". Nothing anywhere keys a MUST on "checkable from the bytes alone".
Attack fails.

## Constructions for a byte-level fork

Actors this document defines: creator, appender, updater, writer, reader,
verifier. I tried each against the R3-vs-R4 routing the clause rationalises.

C1. File F1: user-metadata record, encoding 2, content-size declares 100,
frame decodes to 4096.
  Old text: "a failure to decode within the meaning of R3" → §21.5 row R3 →
  reader | extent use | ignore-record | violation.
  New text: R4 → reader | extent use | ignore-record | violation.
  §21.5 preamble (3536-3538): "Every row here is a violation all the same ...
  never makes the file conforming". [R-CNF-05] bars every conforming writer
  from emitting F1 under BOTH readings. Emittable set does not move. No fork.

C2. Detector/detection-point fork. R3 and R4 are identical in every
register-relevant column: detector reader, detected "extent use", outcome
ignore-record (fixed for the whole of §21.5 by [R-CNT-25]'s quarantine, §21.1
3299-3300). [R-CNF-04]'s duty ("MUST detect every violation the register
assigns to the reader as its detector") fires identically. No fork.

C3. Verifier verdict fork. A verifier that declines the decode → "cannot
establish" and MUST NOT certify (2487-2492), identical under both routings;
§21.5's preamble scopes the decline exception to "the size bound or ... the
frame's declared window" (3529-3531) and NOT to the content-size field, so the
mismatch stays a fact about the file under both. A verifier that does decode
reports *nonconforming* under both. No fork.

C4. Bound-interaction construction (the one I thought would work). F2:
content-size declares 8 KiB; the frame actually decodes to 32 MiB; §21.9's
user-metadata guarantee is 16 MiB (line 3689). Reader A, bound 16 MiB: cannot
use content-size to size a buffer (carry-over bar), decodes, hits its bound,
ignore-record on capability grounds, file "remains conforming" *on that
ground*. Reader B, bound 64 MiB: decodes fully, sees the mismatch, R4,
ignore-record, file nonconforming. Two readers differ — but they differ
identically under the OLD text, where the same file was an R3 violation A
equally could not reach, and both readers emit the same outcome class
(ignore-record) for the record. The divergence is A's inability to establish,
which [R-CNF-11] already handles, and it is not created or removed by the
clause. No fork.

C5. Single_Segment_Flag construction. With SSF set, RFC 8878 derives
Window_Size = Frame_Content_Size (the Note at 2298-2300). §18.2 leaves
Window_Size to the reader and says a too-wide window is "no violation ... the
file exceeds a §21.9 guarantee and so remains conforming", while the
content-size sentence makes a mismatch a violation. I hoped for a conforming
file that one reading permits and the other bars. It collapses: if
content-size is honest, Window_Size = decoded length and there is nothing to
route; if content-size lies, the file is nonconforming under both readings.
No fork.

C6. De-addressing / supersession move (the charter's first standard attack).
Leave the damaged extent out of the live state — supersede the record, turn
the extent to slack. Then no row fires at all, under BOTH readings equally,
because R3 and R4 have the same detection point ("extent use") on the same
structure. The move that rescues a byte-level finding when only one reading
registers the condition does nothing when both do. No fork.

C7. Updater/appender carry-forward. [R-CNF-06] makes an updater a writer for
the bytes it produces and §20.4 makes it preserve records it does not
understand; a latent violation carried forward is a violation under both
readings alike (2890-2894). No fork.

## Conclusion

The clause is a rationale sentence attached to an untouched normative MUST
("when present it MUST equal the byte length of the decoded document",
2479-2481). It is body prose, not a blockquote, so [R-CNF-01] does not dispose
of it — the verifier was right about that and right not to lean on it. But
under every construction I could build, the file at issue is nonconforming
under both the old and the new routing, both routings assign the same detector,
detection point and outcome, and no normative duty anywhere in the document
keys on the phrase. The emittable set does not move and no accept/reject
verdict turns on it.

The auditor's own byte-level grade was "not byte-level" and the auditor was
right. The stronger result is that the substantive complaint also fails:
routing to R4 is what MAKES the condition decoder-independent, which is what
the clause claims and what [R-CNF-02] warrants.

Residual (non-byte-level, and outside X-03's scope, recorded not asserted):
hunk 1's new exhaustive carry-over now imports "no dictionary use, disclosed
or not" into §18.2, and R4's condition cell registers "one of the frame
constraints §18.2 states or carries over" with detector "reader" — while
§17.2 (2280-2283) and §21.7 (3608-3611) both classify undisclosed dictionary
use as not detectable by inspection. That is a detector question, not a
content-size question, and I did not develop it.

VERDICT: DOWNGRADE_STANDS. Byte-level: no.
