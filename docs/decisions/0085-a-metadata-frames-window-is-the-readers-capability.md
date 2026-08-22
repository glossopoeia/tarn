# 0085. A metadata frame's window is the reader's capability, not the file's defect

- Status: Accepted (resolves round 20's byte-level finding)
- Date: 2026-08-21
- Covers: §18.2's encoding-2 frame constraints; the R3/capability boundary for
  a declared `Window_Size`
- Confirm: none

## Context

Round 20 returned one byte-level ambiguity, and it is the **constructive
adversary's first survivor in fifteen rounds** — a role that has come back
empty or refuted-from-the-text since round 5, where it tried 23 attacks and
refuted every one.

§18.2 makes encoding 2 "exactly one RFC 8878 compressed frame" and withdraws
§17.2's window constraint, correctly: that constraint is stated "against a
tile's declared decoded size", and a document has no declared size. But the
withdrawal left the frame's declared `Window_Size` governed by nothing, while
§21.9 guarantees a conforming reader only **8 MiB** of it — a quantity §21.9
lists separately from the 16 MiB it guarantees for a document's *decoded size*.

So a reader that cannot decode such a frame has either established §21.5's R3
("a user-metadata document's stored bytes fail to decode under its declared
assigned encoding") or hit its own capability bound, and nothing said which.

**The construction is what makes it byte-level.** The adversary built two
conforming 128-byte files differing only in the Window_Descriptor byte. The
refuter then rebuilt it at *minimal gap* so the answer could not turn on the
size of the excess: `0x68` is windowLog 23, exactly 8 MiB; `0x69` is 9 MiB.
**One bit of a mantissa field separates a file every conforming reader MUST
accept from the disputed one**, and the two readings give it opposite verdicts
— *nonconforming* under R3, *cannot establish* under the capability reading.

## Decision

**The window takes the treatment the same sentence already gives the decoded
size.** §18.2 already says a reader "decodes with a bound of its own choosing,
no smaller than §21.9's user-metadata guarantee, and a document exceeding that
bound is ignore-record like any other it cannot read." The window is now stated
to be unconstrained here for the same reason and to take the same treatment: a
reader's window bound is its own, no smaller than §21.9's guarantee for that
quantity, and a frame declaring more is **ignore-record on that ground — the
reader's capability, not a failure to decode within the meaning of R3, and no
violation.**

`[R-MTA-09]` is the model and is cited: it already settles that declining a
metadata document on a size bound "is that verifier's capability and not a
limit on validity". `[R-ERR-03]` supplies the general frame — §21.9's table
states **minimum guarantees, not caps**, and "A file exceeding any of these
remains conforming, and a reader MAY decline it."

Row R4 is deliberately untouched. It registers a break of the frame
constraints §18.2 states or carries over from `[R-COD-06]` — frame magic, no
skippable frame, no second frame, no nonzero dictionary ID, no content-checksum
flag — and the window is not among them, so R4 neither gains nor loses a case.

## Consequences

The register does not grow. This is the second time a §21.9 guarantee has had
to be told apart from a violation — `[R-MTA-09]` did it for the decoded size,
and this does it for the window — which suggests the distinction is worth
stating once generally rather than per quantity. That is not done here: §21.9's
table lists eight quantities and only two have ever been confused with
violations, so a general rule would be written ahead of its evidence.

**Round 20 is also the first round measured without contaminated agent
context** (ADR-0084), and its numbers are the cleanest the project has: 20
findings over 16 distinct defects, the lowest recent counts, with quiz 15/0/0
for the fourteenth round running.

## Precedent

- `[R-MTA-09]`, which decided the identical question for the neighbouring
  quantity and supplied both the reasoning and the wording.
- `[R-ERR-03]`'s "minimum guarantees, not caps", which is why a file exceeding
  one stays conforming and the refusal lands on the actor.
