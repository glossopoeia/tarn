# 0065. Seven decisions round seven escalated

- Status: Accepted
- Date: 2026-08-11
- Covers: verdict priority; §21.9 composition; the layer-name namespace under a
  framing failure; F5/L3's qualification; slab continuity across a rejected
  entry; the slack total under an elective stop; `[R-VEC-04]`'s intact sibling
- Confirm: none

## Context

Cleanroom round 7's editorial pass refused 13 repairs on the ground that each
would change what a file may contain or what an implementation must do. Analysis
against the document and the ADRs reduced them: **five were already decided** by
rules nobody had connected, **one was not a defect**, and **seven are genuine
decisions**. Those seven are recorded here. The six are editorial and land
alongside, cited in `docs/cleanroom/07-g3/findings.md`.

## Decision

**A verifier that has established a violation reports *nonconforming*.** *Cannot
establish* is reserved for a traversal that established none; a requirement the
verifier could not check is carried in the report, as ADR-0062 carries an
unexamined scope. Priority now runs to the verdict a file's own bytes earn.
§22.1's adversary otherwise had a suppression primitive: appending one 17 MiB
user-metadata document downgrades any budget-limited verifier from
*nonconforming* to *cannot establish*, cheaply and under the attacker's control.

**§21.9 gains a directory-region-size row.** The limits table's rows bound one
quantity each and nothing bounded their product, so a file at 65,536 layers of
4,096 channels forces a reader to materialize a 1.6 GB directory while remaining
one it MUST accept. The new row bounds the resource §19.1 actually obliges a
reader to fetch whole, which is the method ADR-0043 used for every other row.

**A name a reader cannot obtain is not in the namespace.** §19.1 step 4 builds
the layer-name namespace from the name fields §7.4's framing yields; a layer
record whose name field does not lie entirely within `inline_length` contributes
no name and is a validity error at layer scope (`[R-CNT-18]`). Stated as a
namespace rule, not an ordering rule, so ADR-0058's "uniqueness first, over raw
bytes" keeps its meaning for every name that exists.

**F5 and L3 stay, qualified.** Both name a width error with total size
unchanged, which no file exhibits in isolation. They gain F1's self-qualifying
clause and T13/T26's delegation sentence naming the rows whose value gates
actually fire. F5's trailer instance is rewritten regardless of that: the
editorial pass replaced it with *"a single u32 written across the version_major
and version_minor slots"*, and those bytes read back as `version_major = 1,
version_minor = 0` — a conforming trailer, so `[R-CNF-02]` makes the instance
describe a valid file. TV-0114 is rebuilt to match.

**§15.3's removal clause is scoped to the six structural grounds.** A tile that
fails only its own CRC keeps its extent for the slab invariant, §7.2's overlap
rows and `[R-LIF-08]`'s slack total. Under the unscoped reading one flipped bit
escalated reject-tile to reject-layer — removing a present tile from a run makes
its innocent neighbours look non-contiguous — and `[R-SLB-03]`'s stated reason
for sentinel transparency, *"they occupy no bytes and do not break packing"*,
does not transfer to a tile that occupies its bytes and breaks nothing.

**A verifier that stops early still owes a bounded slack total.** §5.2's escape
covers any incomplete walk, and a partial total counts only unclaimed bytes
inside regions actually walked; a verifier reporting one MUST also report the
byte extent of the regions it did not walk. This keeps ADR-0062's shape — permit
the stop, require the report to name its own boundary — rather than re-deciding
it in a second place.

**`[R-VEC-04]`'s intact sibling cuts on serveability.** A tile of the same layer
discharges the sibling only where that layer is one a reader may still serve.
Cutting by outcome class instead would assert something false about the nine
verifier-detected reject-layer rows, where the layer remains servable.

## Consequences

The §21 register stays **125 conditions over 252 instances** and the corpus stays
at **305 vectors** with 100% per-instance coverage. §21.9's new row is a limits
row, not a register condition, so it adds no instance and owes no vector. TV-0114
is rebuilt in place; three manifest entries gain co-exhibited rows under
`[R-VEC-02]`.

Priced knowingly, three times. The directory row removes files from the set every
conforming reader must open, which is a real cut to the portability floor ADR-0043
sold to writers. The F5/L3 qualification leaves three rows a verifier built from
§21 alone cannot turn into a check of its own, and makes §21.8's coverage lean on
`[R-VEC-02]`'s co-attribution clause. And splitting §15.3's grounds costs the
clean single class: an implementer now has to know which of seven grounds it is
looking at before deciding whether an extent is still a claimant.

## Precedent

- ADR-0062, whose separation of what a report must say from what the verdict is
  supplies the shape for both the verdict-priority and slack-total decisions.
- ADR-0043's cost-budget method for the limits table, applied to the one resource
  it had not bounded.
- ADR-0058, which fixed the front-block obligation on a structural test rather
  than an economic one; the namespace decision follows it by turning an ordering
  question into a question about what exists.
- ADR-0046, under which the specification governs and a disagreeing vector is
  corrected — the authority for rebuilding TV-0114.
