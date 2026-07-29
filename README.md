# TARN — Tiled Array, Random-access, N-dimensional

> One file. No infrastructure. A tiled N-dimensional array format you can
> read in an afternoon and implement in a weekend.

What SQLite is to Postgres, TARN is to [Zarr](https://zarr.dev): a
single-artifact, zero-infrastructure array container — space-efficient,
integrity-checked by default, efficient to read partially over plain HTTP
range requests, and laid out for GPU-friendly I/O. Zarr, HDF5, and
cloud-optimized GeoTIFF are excellent tools at different points in the design
space; TARN exists for the case where you want exactly one file, a dumb file
server, and a spec small enough to hold in your head.

**Status: pre-1.0, in design.** The specification is being developed in the
open and nothing here is stable yet. Current phase: planning — see
[PLAN.md](PLAN.md) for the roadmap and
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) for what is still undecided.

## Design pillars

- **Single file, dumb storage.** Any static file server or object store
  suffices; there is nothing to operate.
- **Integrity by default.** Every byte of metadata and payload is covered by
  a checksum, and verification is a reader obligation, not a suggestion.
- **O(1) remote open.** All metadata is reachable in a bounded number of
  range requests, stated as a testable guarantee.
- **GPU-friendly layout.** Uniform tiles, optional alignment for
  O_DIRECT/GPUDirect/mmap, and slabs — aligned contiguous tile runs treated
  as single I/O units.
- **Small, closed spec.** One document, one conformance profile, no optional
  dialects: every conforming reader opens every conforming file.

## Non-goals

- **Not a database.** No transactions, no queries, no concurrent writers. If
  you need those, use a database.
- **Not an image format.** No colorspace or rendering semantics in the core;
  domain conventions live in registered metadata keys.

## Repository map

| Path | What it is |
|------|-----------|
| [PLAN.md](PLAN.md) | How this spec is being built: success gates, drafting order, process |
| [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) | The open-decision ledger |
| [docs/decisions/](docs/decisions/) | Architecture Decision Records — the reasoning trail |
| [docs/research/](docs/research/) | Distilled lessons from PNG, TIFF, Zarr, PMTiles, and QOI |
| [AGENTS.md](AGENTS.md) | Working instructions for contributors and their tools |
| `spec/` | (Phase 2) The specification and ID registries |
| `conformance/` | (Phase 2) Test vectors with expected outcomes |

## How this project uses AI

TARN is developed with substantial AI assistance, used under human direction
for research, drafting, adversarial review of specification text, and
cleanroom implementability testing. All design decisions are made, reviewed,
and owned by the maintainer; design authority and final editorial control
rest with the maintainer, not with any tool. The reasoning behind every
significant decision is recorded in
[docs/decisions/](docs/decisions/), so the trail is auditable
independent of how any given sentence was drafted. Errors are the
maintainer's responsibility.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — including the decision process and
the AI-assistance policy for contributions.

## License

| Content | License |
|---------|---------|
| Specification text and documentation (`spec/` when present, `docs/`, and all repository documentation files) | [CC BY 4.0](LICENSE-SPEC) |
| Schemas, tooling, conformance harness | [Apache-2.0](LICENSE) |
| Binary conformance vectors (Phase 2) | CC0 1.0 (planned — see [ADR-0016](docs/decisions/0016-licensing.md)) |
