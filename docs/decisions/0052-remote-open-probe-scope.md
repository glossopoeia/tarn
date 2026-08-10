# 0052. The remote-open prober, and where tooling stops being a reader

- Status: Accepted
- Date: 2026-08-09
- Covers: extending ADR-0050's tooling scope to cover gate G4's harness and a
  file builder; the line between a prober and a conforming reader
- Confirm: none

## Context

Gate G4 asks for this specification's cold-read accounting to be
"demonstrated against a dumb HTTP server, with request counts matching
the stated guarantee." A demonstration needs three things this
repository did not have: files to serve, a server that answers byte
ranges and nothing else, and something that performs §19.1's open while
counting round trips.

The third is the problem. Counting requests means walking the open —
validating a trailer, verifying a directory CRC, framing records. That
is most of a reader's front half, and ADR-0050 drew its line at "No
reader, no decoder — a reader in this repository would become the de
facto definition of conformance, which ADR-0046 exists to prevent."
ADR-0050's scope covers the specification's mechanical gates and
nothing else, so G4's harness needs its own decision rather than a
generous reading of that one.

## Decision

- **ADR-0050's scope extends to two further programs** under
  `conformance/tools/`, on the same terms: they read the specification
  or emit bytes, they add no dependencies beyond the standard library,
  and they are testable against artifacts the specification itself
  prints.
- **`tarn_build.py` emits, never reads.** It constructs conforming
  files from explicit declarations. It parses no TARN file and passes
  judgement on none. Its acceptance test is Appendix A: it must
  reproduce the printed hex dump byte for byte, and reproduce §4.5's
  CRC check vectors. It is also the seed builder gate G5 will need.
- **`tarn_probe.py` is a prober, not a reader.** The line: it performs
  §19.1's open — trailer, directory, record walk far enough to count
  layers — and stops. It fetches no tile index, decodes no payload,
  returns no sample, and pronounces no file conforming or
  nonconforming. Everything a reader does *after* the open is what
  makes a reader the definition of conformance; a program that stops at
  the open measures I/O and settles nothing.
- **The harness measures strategies, not readers.** §6.4 states counts
  for a baseline and a speculative variant; the prober implements those
  as named modes and reports what each costs. It never asserts that a
  count other than the one it measured would be nonconforming, because
  no rule says so — see the consequence below.

## Consequences

G4 becomes measurable, and the measurement is reproducible by anyone
with a Python interpreter: `python3 conformance/tools/tarn_probe.py`.
The builder that G5 needs arrives early and arrives tested, which is
the same economy that made the G4 fixtures double as corpus seeds.

Priced knowingly, and this is the finding the exercise produced: the
prober cannot fail a reader, because §6.4 bounds no reader. Its
keywords are MAY (speculation), SHOULD (the writer's window budget),
MUST (handling a 200), SHOULD (the no-suffix fallback), and MUST /
MUST NOT (size authority). "The baseline remote open is two requests"
is declarative prose. A reader that takes §19.1's numbered steps
literally on a transport without suffix ranges performs three round
trips and violates nothing — the harness measures exactly that, as
mode M5. So the harness demonstrates *achievability*, not conformance,
and G4's own wording has to say which it means before the gate can be
called passed. That is a decision about the specification, recorded
here as the reason this ADR does not itself declare G4 met.

The prober's own conduct is constrained by the same reasoning: because
it is not a reader, a file it opens without complaint is not thereby
evidenced as conforming, and the G4 record says so.

## Precedent

- ADR-0050, whose scope this extends and whose reasoning it inherits.
- ADR-0046's derivative corpus: the specification is the fixed point,
  and a tool in this repository must never become a second authority.
- PLAN.md §2's standing rule that this repository never depends on an
  implementation — which a prober that stopped at the open does not
  become, and a reader would.
