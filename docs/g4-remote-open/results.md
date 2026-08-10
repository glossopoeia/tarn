# G4 — O(1) remote open: measurement record

Gate G4 (PLAN.md §1): *"The spec's normative cold-read accounting is
demonstrated against a dumb HTTP server, with request counts matching the
stated guarantee."*

Reproduce with:

```bash
python3 conformance/tools/tarn_probe.py
```

Method: files built by `tarn_build.py` from the specification's own rules,
served by a byte-range HTTP server that does nothing else, opened by a prober
that performs §19.1's four steps and stops (ADR-0052). No tile index is
fetched, no payload decoded, no sample returned.

## What was measured

Six files. Case C and D are adjacent 64-aligned files straddling §6.4's
65,536-byte discovery window — the same 617 layers, differing only in the last
layer's name length.

| Case | File | Size |
|---|---|---|
| A | Appendix A's minimal file, no layers | 128 B |
| B | one layer, 4 stored tiles | 320 B |
| C | window `F − dir_offset` = 65,520 — just inside | 65,536 B |
| D | window `F − dir_offset` = 65,584 — just outside | 65,600 B |
| E | one 16 MiB tile, one layer | 16,777,472 B |
| F | 512 layers | 51,840 B |

Five transport/strategy modes: **M1** exact-target baseline; **M2** speculative
64 KiB suffix with containment; **M3** no suffix-range support, windowed;
**M4** a server that ignores `Range` and answers 200; **M5** no suffix-range
support with §19.1 followed literally.

## Results

| Mode | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| **M1** exact-target | **2** | **2** | **2** | **2** | **2** | **2** |
| **M2** speculative suffix | 1 | 1 | 1 | **2** | 1 | 1 |
| **M3** no suffix-range, windowed | 2 | 2 | 2 | **3** | 2 | 2 |
| **M4** server ignores Range (200) | 1 | 1 | 1 | 1 | 1 | 1 |
| **M5** no suffix-range, §19.1 literal | **3** | **3** | **3** | **3** | **3** | **3** |

Bytes fetched, selected:

| Case | M1 | M2 | M4 |
|---|---|---|---|
| A (128 B) | 68 | 128 | 128 |
| E (16,777,472 B) | **185** | 65,536 | **16,777,472** |
| F (512 layers) | 51,780 | 51,840 | 51,840 |

## What holds

**The invariance claim holds.** `[R-RDR-01]` says the open's I/O is §6.4's
accounting "at any layer count and file size." M1 is 2 requests across five
orders of magnitude of file size (128 B → 16.7 MB) and 0 → 617 layers. Case E
opens a 16.7 MB file having fetched **185 bytes**.

**The window boundary behaves exactly as §6.4 describes.** C and D differ by
64 bytes of file length and nothing else; C's directory is contained in a
64 KiB suffix and costs one request, D's is not and costs two — which §6.4
already states is conforming: *"a larger directory is conforming and merely
costs the second request."* D is not a failure.

**Nothing was fetched that the open does not consume.** No request touched a
tile index, an extent, or a payload, as `[R-RDR-01]` and `[R-RDR-02]` require.

## What the measurement found

Three findings, each reached independently by agents deriving expected counts
from the text alone, before seeing these measurements. The first was
miscalibrated and is retained with its resolution, because the error is
instructive; the other two led to edits.

### G4-1 — No rule bounds a reader's request count (resolved: not a defect)

§6.4's BCP 14 keywords are MAY (speculation), SHOULD (the writer's window
budget), MUST (handling a 200), SHOULD (the no-suffix fallback), MUST and
MUST NOT (size authority). *"The baseline remote open is two requests"* is
declarative prose, and **M5 measures a reader that takes three round trips on
every case and violates nothing.**

This was first recorded as a gap in the specification. It is not. §6.4 places
its MUSTs exactly where a reader can be *wrong* — transport handling and size
authority — and leaves alone everything where a reader is merely *different*.
Which strategy is better is a property of the transport, not of the file: a
high-latency link rewards fewer, larger requests and a metered one rewards the
opposite, and a format that legislated the choice would be dictating I/O
strategy to every deployment.

The mismatch was in the gate's own wording, which called the accounting
"normative" and its counts a "guarantee". PLAN.md §1 now states G4 as the
**working-set invariant** — the open consumes the trailer and directory and
nothing else, at any file size and layer count (`[R-RDR-01]`) — with request
counts as illustration. That is the claim that binds readers, that is a
property of the format's structure rather than of anyone's strategy, and it is
the one the measurement actually establishes. §6.4 gained a note saying so, so
the next reader does not repeat the inference.

### G4-2 — The two-request baseline was circular as written (fixed)

§6.4's request 1 is *"fetch the final 64 bytes"*, an exact target that cannot
be addressed without knowing F. §19.1 makes obtaining F its own numbered step 1
and only then fetches `[F − 64, F)` at step 2. The count of two is recoverable
only by chaining §6.4 with `[R-CNT-10]`'s *"the complete length of a range
response"* and `[R-RDR-01]`. The word *suffix* never appears in the baseline —
it appears only in the speculative option and the fallback clause.

A reader implementing §19.1 in its stated order performs a size probe, a
trailer fetch, and a directory fetch. That is M5, and it is three requests.

**Fixed.** §6.4's request 1 now names itself a suffix range whose response
carries F, and §19.1's step 1 now says the steps are ordered by dependency
rather than by I/O — so a reader following either text literally arrives at
the same two requests. Neither edit adds a requirement; a three-request open
remains conforming, as G4-1 records.

### G4-3 — "O(1) remote open" is O(1) in requests only

Nothing bounds the open's byte volume. `[R-CNT-10]` permits a reader meeting a
200 to *"accept the full body deliberately"*, which is one request — the best
score in the table — at a cost of the whole file. **M4 on case E: one request,
16,777,472 bytes**, to read a 185-byte directory. A gate scoring only round
trips ranks that reader above the baseline.

## Verdict

**G4 passes**, on the claim PLAN.md §1 now states.

The working-set invariant is demonstrated: across six files spanning five
orders of magnitude of size and 0 to 617 layers, and five transport
strategies, **no request in any mode touched a tile index, an extent, or a
payload**. The open consumes the trailer and the directory, and nothing else,
exactly as `[R-RDR-01]` claims — which is a property of the format's
structure, so no reader's strategy can spoil it.

The request counts are recorded as illustration of what that costs a reader
fetching exactly what it needs: two, invariant across every file measured,
opening a 16.7 MB file on 185 bytes. They bound no reader, and M4 and M5 are
in the table precisely to show conforming readers that spend more.

What G4 does **not** establish, stated so it is not assumed: that any
particular implementation is efficient, that byte volume is bounded (G4-3), or
that a reader exists at all. It establishes that the format's discovery
structure permits a constant-cost open, and that a program stopping at §19.1's
open needs nothing else.
