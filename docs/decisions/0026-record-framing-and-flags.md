# 0026. Record framing: 24-byte header, MU/PE flags, no embedded offsets

- Status: Accepted (resolves Q-G2)
- Date: 2026-07-30
- Covers: directory record header; must-understand/preserve semantics;
  updater obligations
- Confirm: none (the structural scope-binding mechanism — nesting vs a
  framing-level layer field — is fixed in the directory section's
  drafting, under the normative constraint below)

## Context

Forward compatibility lives or dies on what a tool may do with a record it
does not understand. The proven design is explicit per-record property
bits (PNG), refined by a banned list of facts that may never be ignorable
(Zarr's must_understand), and completed by something neither had: a rule
making *editing around* unknown records decidable — because TARN
explicitly supports re-taggers, appenders, and compactors (ADR-0003's
updater class, ADR-0017's append model).

## Decision

**Header, 24 bytes fixed:** `type u16 · flags u16 · inline_length u32 ·
extent_offset u64 · extent_length u64`. Flags: bit 0 = MUST_UNDERSTAND,
bit 1 = PRESERVE_ON_EDIT, bits 2–15 reserved (writers zero, readers
ignore). Small payloads inline in the directory; bulk payloads live in the
extent slot ((0,0) = none — unambiguous, offset 0 is the front block). The
extent slot carries its own invalid-combination table (half-null forms,
front-block/trailer intrusions, overlap — folded into ADR-0024's
exactly-once partition).

**Flag authority.** The registry fixes flags for registered types; readers
apply spec semantics for known types regardless of stored bits (a flipped
bit never changes conforming behavior; verifiers report mismatches).
Stored flags are authoritative **only for unknown types** — their job is
to travel with records the consumer has never heard of. MU=1 ∧ PE=0 is
forbidden (it licenses silent deletion of critical meaning); tools
encountering it treat it as PE=1.

**Scope is structural.** Every record attaches to file scope or exactly
one layer, determinable **from framing alone, without parsing the
payload** (normative constraint; mechanism fixed in drafting). Unknown MU
at layer scope → reject-layer, never the file; at file scope →
reject-file. Ancillary records MUST NOT depend on other ancillary records.

**Banned-ancillary criterion and floor.** A type may register MU=0 only if
ignoring it leaves every stored sample bit-exact and geometry identical.
Never ancillary: sample type · geometry · channel set/layout · codec,
filter, parameters · linearization · fill · index location/encoding · any
payload-interpretation transform.

**No embedded offsets.** An MU=0 record's only file-extent reference is
its header slot — never offsets inside its payload or extent contents.
All other extent references live in MU=1 registry-reviewed types. This is
the compactor's load-bearing wall: it can relocate an unknown ancillary's
bytes (copy extent, rewrite the slot it *does* understand) without
parsing them. Residual, stated honestly: the rule is unverifiable for
unknown types — a nonconforming experimental record embedding offsets
gets no relocation guarantee; compactor output is conforming regardless;
verifiers report unknown-with-extent as unverified (PNG's private-chunk
residual, named).

**Updater obligations.** All edits follow ADR-0017 (append new directory +
trailer; nothing moves except under compaction). A tool MUST fully parse
the trailer, record framing, and every record of any layer it modifies
(which keeps declarations like ADR-0022's slab honest). Unknown records:
MU0/PE1 → copy verbatim; MU0/PE0 → drop when modifying its scope
(reported), preserve otherwise; MU1 → copy verbatim and MUST NOT modify
the scope it governs — a file-scope unknown critical blocks file-scope
edits entirely; compactors refuse on any unknown MU1. The full
flags × conformance-class table lands in the spec.

## Consequences

Re-taggers and appenders operate with framing-level parsing only;
compaction is a decidable procedure instead of folklore; new ancillaries
(stats, provenance) can be megabytes without touching the discovery
window. Costs: 16 slot bytes per record (~5 KB per 300 records — noise),
and registry review carries real gatekeeping weight (flags + offset rule
checked at registration).

## Precedent

- PNG §5.4/§14 property bits and editor rules, minus the case-encoding
  trick (literal bits, tested bitwise).
- Zarr's must_understand with a banned-ancillary list.
- The safe-to-copy problem PNG left half-solved — closed here by the
  extent slot + no-embedded-offsets rule.
