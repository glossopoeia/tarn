# 0043. Limits are minimum guarantees, sized by cost budgets

- Status: Accepted (resolves Q-H1)
- Date: 2026-08-05
- Covers: the §21.9 limits table; which quantities get rows and at
  what values; the hard caps it sits beside
- Confirm: none

## Context

`[R-CNF-10]` already fixed the *model*: every limit affecting file
validity or reader acceptance lives in this specification, readers
MAY enforce resource limits, and readers MUST accept conforming
files within the stated minimums. What remained was which quantities
get rows and at what numbers — a decision that is arbitrary unless
the numbers come from somewhere. Two sources are available: existing
ecosystem convention, and the points where this format's own
structures change cost character.

## Decision

- **Resource limits are minimum guarantees, not hard caps.** A file
  exceeding a row stays conforming; a reader MAY refuse it for
  resources, while software refusing a file within every row is not
  a conforming reader. Either refusal MUST be reported as a resource
  limit rather than as invalidity — the two send users to opposite
  remedies. Hard caps exist only where a field's width forces one
  (a 255-byte name behind a `u8` prefix, `[R-ENC-12]`; rank and
  channel count behind §7.4's `u8` and `u16`), where an external
  format imposes one (lz4's `0x7E000000`, `[R-COD-07]`), or where
  the value domain does (2⁶³ − 1, `[R-ENC-03]`).
- **The rows, and where each number comes from:**
  rank 32 and channels 4096 — NumPy and HDF5's long-standing rank
  ceiling, and roughly double the band count of hyperspectral
  instruments; addressed tiles per layer **2³²** — a budget point in
  this format's own index: the segment-CRC array a reader must fetch
  whole before using any entry grows linearly at 4 bytes per 2¹⁶
  entries, and 2³² is where it is still 256 KiB (4 MiB at 2³⁶,
  64 MiB at 2⁴⁰); layers 65,536 — a directory around
  12.5 MiB, past which the discovery budget degrades; decoded tile
  size 256 MiB — an order above the 1–16 MiB working range now
  recorded in spec §11.3, so the guarantee never binds ordinary
  files; user-metadata document
  16 MiB; zstd `Window_Size` 8 MiB — RFC 8878's own recommended
  decoder support, which stock encoder defaults stay within.
- **Every row gets an at-limit conformance vector** where one is
  constructible, per Q-H1's settling condition. The entry_count row
  is the exception: at 2³² its index region alone is ~80 GiB of
  incompressible entries, so it is exercised by a scaled vector — a
  layer whose segment-CRC array spans several segments — with the
  bound itself checked by arithmetic rather than by bytes.

## Consequences

Writers gain a portability floor they can target without negotiation;
readers gain explicit licence to cap resources without becoming
nonconforming, provided they say which kind of refusal it is. Nothing
at scale is foreclosed: a 2³⁴-tile array is a valid TARN file that
some readers decline, rather than a file the format forbids forever.
The cost is that "conforming file" and "file this reader opens" are
not the same set — stated plainly rather than hidden, since the
alternative is limits living only in implementations, which is the
condition `[R-CNF-10]` exists to prevent.

## Precedent

- RFC 8259 §9's implementation-limits pattern (implementations may
  set limits; the specification names what interoperable senders can
  rely on) as the direct model.
- NumPy's and HDF5's rank ceilings; RFC 8878's recommended decoder
  window support.
- TIFF's optional-everything ceiling as the counterexample: limits
  that live only in readers make "valid file" a per-reader question.
