# Refute pass — R28 finding: L23 Detected cell (layer access) vs §19.1 step 4 / §19.2 (open)

Verdict: NOT_BYTE_LEVEL.

## Disclosure

Read exactly one file: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md,
via `sed -n` ranges and `grep -n` against that file only. Ran no other file reads, no git,
no web, no directory listings, no conformance tooling, no registry.json. No local computation
was needed (no CRC or arithmetic construction survived far enough to need it).

Unsolicited context appeared before I began: a project-instruction block, an environment
block naming the repository/branch/recent commit subjects, a user-email line and a date line.
I disregarded all of it and do not repeat its contents. I did not open AGENTS.md or any doc
it pointed at.

## Sections opened

§2.1 (BCP 14 scope), §2.2, §2.3 (conformance classes: [R-CNF-02]–[R-CNF-06], [R-CNF-11]),
§2.4 (outcome classes, [R-CNF-07]–[R-CNF-09], [R-CNF-12] and its closing Note),
§2.5; §4.6 ([R-ENC-11]–[R-ENC-15]); §4.7; §7.4 (the layer-record table, [R-CNT-23],
[R-CNT-16], [R-CNT-17], [R-CNT-18]); §19 preamble; §19.1 (all four steps, [R-RDR-01]);
§19.2 ([R-RDR-02] + its Rationale); §19.3 ([R-RDR-03]); §19.4 ([R-RDR-04]);
§20.3 (the append procedure, [R-WRT-03], steps 1–4); §20.4 ([R-WRT-05], the stored-flags
table, the "No commit therefore removes a layer record" paragraph, [R-WRT-08]);
§20.5 ([R-WRT-06], [R-WRT-07], [R-WRT-09]); §21.1 (how to read the register, in full);
§21.2 rows F1–F10, F12, F13, F23–F36 (F4 in particular); §21.3 rows L1–L29 (L3, L5, L6,
L14, L23, L24 in particular); §21.5 rows R3–R10; §21.6; §24 ([R-VEC-01]–[R-VEC-04] and Note).

## The dispute, restated

L23 (§21.3): condition "A declared region of the layer record's inline payload does not lie
entirely within inline_length (overrun or truncation)", instances "leading fixed fields
(name … C); d dimension entries; C channel entries; trailing fixed fields", Detector reader,
Detected **layer access**, Governing rule [R-CNT-18].

§19.1 step 4 (inside [R-RDR-01], the open algorithm): "The layer-name namespace is built from
the name fields a reader can obtain under §7.4's framing: a layer record whose name field does
not lie entirely within that record's inline_length yields no name field to compare, so it
contributes no name to the namespace and is instead a validity error at layer scope
(`[R-CNT-18]`)."

§19.2 first bullet lists "the layer-name namespace (§19.1's steps)" under **at open**.

Two readings: (1) the name-field instance of L23 is due at open; (2) it is due at layer access.
Question: does the choice move emitted bytes, or an accept/reject verdict?

## Constructions tried

### C1 — reader pair, request against an untouched sibling layer
File: layers A and B. A's layer record has inline_length too small to hold its name field
(e.g. inline_length = 4 with name length prefix 0x0A). B is well-formed with one stored tile.
Reader P detects at open; reader Q defers to layer access and the request never touches A.
Killed: outcome is reject-layer under both — §19.1 step 4 names the scope itself ("a validity
error at layer scope ([R-CNT-18])") — and §19.2's closing sentence says the deferring reader is
conforming for B: "a violating record in a layer never accessed leaves every other layer's
reads conforming." Identical bytes returned for B; A is never served under either.

### C2 — request against the damaged layer A
Killed by §19.3: "A reader's **first access** to a layer … MUST be preceded by full validation
of the layer record — extent slot and inline payload both … the exact parse, sub-record walk,
and sub-record multiplicity (`[R-CNT-18]` …)". The deferring reader hits L23 at layer access,
before returning any sample. Reject-layer under both; no byte of A is returned under either.

### C3 — duplicate layer name (F4 / [R-ENC-15], reject-file) escalation
Layer A's name field overruns inline_length but the length-prefixed bytes it *declares*, read
past inline_length, are byte-identical to layer B's name. Under a permissive reading the reader
would compare them and reach reject-file (file scope) instead of reject-layer.
Killed twice over: §19.1 step 4 excludes A from the namespace outright ("yields no name field
to compare, so it contributes no name to the namespace"), and that sentence belongs to
[R-RDR-01], not to L23 — the row's Detected cell cannot reach it. F4's own row carries the same
guard: "both obtainable within their records' inline_length". So the namespace, and therefore
the F4 verdict, is the same set of names under both readings.

### C4 — degenerate file: a single layer, damaged
One layer only, name field overrunning. Killed: no rule turns "every layer is reject-layer"
into reject-file; §21.6 even lists "The file contains zero layers | A conforming file with an
empty directory". Addressing A by ordinal rather than by name still routes through §19.3 (C2).

### C5 — append path, commit that does NOT modify A (the §20.3 step 2 hook)
This is the only clause in the document whose antecedent is *detection at the open*:
"A violation the open establishes bars the commits its outcome bars and no others: reject-file
bars every commit, and reject-layer bars a commit that modifies that layer."
Construction: appender adds a new layer C to the file of C1. Under reading (1) the open
establishes reject-layer(A); under reading (2) it establishes nothing.
Killed: the clause's own consequent makes the two identical for this commit — reject-layer bars
only commits modifying A, and this commit does not modify A. And the same step forbids either
appender from diverging on A's bytes: "Against any other structure the appender carries forward,
it MUST NOT repair the defect … and MUST NOT drop the record (§20.4)", with §20.4's [R-WRT-05]
requiring byte-identical re-emission. Both appenders emit the identical file: A's damaged
record carried forward verbatim, C appended. Not one byte differs.

### C6 — append path, commit that DOES modify A (rename; §20.3 shape (c))
Under reading (1), step 2 bars it outright. Under reading (2), does it slip through?
Killed by [R-WRT-03]: "plus §19.3's layer validation for every layer whose record, index, or
extents the commit modifies" — categorical, so any modification of A forces the §19.3 parse that
detects L23 before emission. And even absent timing: [R-WRT-05] makes "a record it modifies …
new output under its writer obligations ([R-CNF-05])", so the re-authored record must be
conforming, which requires either repair — barred by [R-CNF-04]'s "A reader MUST NOT
heuristically repair a violating structure or infer values this specification does not define",
an updater being a reader (§2.3) — or inventing the unparseable fields. Refusal under both.

### C7 — append path, tiles added to A / A's extents or index changed
Same kill as C6: [R-WRT-03] forces §19.3 on A, and the geometry needed to place entries cannot
be parsed out of a record whose leading fixed fields overrun. Refusal under both.

### C8 — the dropped record rather than the modified one
Drop A entirely in a commit. Killed by §20.4: "No commit therefore removes a layer record …
That is not compaction, which carries every layer of its input forward (§20.5)." Both registered
types carry PE = 1. Dropping a *sub-record* of A instead is licensed only "in a commit that
independently changes the scope the record attaches to: for a layer sub-record, that layer's
record, the entry set of its index, or which of its tiles are stored" — each of which modifies A
and lands back in C6/C7.

### C9 — compaction path (the strongest candidate: refuse vs emit)
§20.5: "A compactor … MUST NOT emit a file carrying a violation **it has detected**" — an
antecedent that is explicitly detection-relative, so if the compactor's obligated depth stopped
at the open, the two readings would fork between "MUST refuse" and "emit the carried-forward
violation" ([R-WRT-01] permits the latter: "a violation latent in a structure it carries forward
verbatim travels into its output").
Killed by [R-WRT-09]: "it relies structurally on every structure it copies, so it MUST verify
each link of the chain — the open (§19.1), **each retained layer's record (§19.3)** and full
index chain … before emitting that structure's bytes." Every layer is retained (§20.4: compaction
"carries every layer of its input forward"), so §19.3 runs on A under both readings, L23 is
detected under both, and since §20.4's table licenses no drop of a layer record, "Where the table
does not license a drop the compactor MUST refuse." Both compactors emit nothing.

### C10 — writer/emittable set
Killed by [R-CNF-02]: "File conformance is a pure predicate on bytes: it does not depend on any
reader, writer, or environment." The L23 condition is a violation under both readings; only its
detection deadline is disputed. [R-CNF-05] therefore bars every conforming writer from emitting
the file under both. The emittable set does not move.

### C11 — conformance corpus / vectors
[R-VEC-02] records "the outcome class (§2.4), the scope, and the §21 register row it exercises
together with that row's governing requirement identifier" — no detection tier. [R-VEC-04]'s
intact-sibling pair is "the scope no reader is permitted to serve and the content a reader that
serves anything at all owes" — identical under both readings. No vector's bytes or expectation
changes.

### C12 — divergence in permitted behavior sets (rejecting the whole file)
Under reading (1) the reader knows at open and may invoke [R-CNF-12] to reject the whole
nonconforming file; under reading (2) it may not yet know. Killed: [R-RDR-02] licenses the early
detection under reading (2) as well — "A reader MAY detect any violation earlier
(`[R-CNF-12]`)" — so both readings admit exactly the same pair of behaviors, and the difference
that remains is diagnostics, which §2.4's Note places outside the bytes: "'Reject' prescribes
the scope of unusability, not user interface: how failure is reported is implementation
technique."

### C13 — could the row's cell even license deferral?
Checked §21.1's definition of the column — "the point **by which** detection is due (§19.2)" —
against §19.2's "no later than … A reader MAY detect any violation earlier" and its Rationale
("The rule fixes the *latest* detection point"). The column is a deadline, so a reader obeying
§19.1 step 4 at the open satisfies the row's cell early; the two texts are compatible rather
than contradictory. §21.1's tie-breaker ("where a row and the rule it cites diverge, the rule
governs") is available if they are read as diverging, and it points at [R-CNT-18]/§19.1 — the
reporter's own reading — so even the divergence branch closes on one answer.

### C14 — the non-name instances of L23
A record whose name field fits but whose later leading fixed fields (through C), dimension
entries, channel entries or trailing fixed fields overrun is untouched by §19.1 step 4 (its name
IS obtainable, so it does contribute a name), and is unambiguously layer access under both
readings. Nothing to fork.

## Conclusion

Every actor pair converges. Readers: same bytes returned, same reject-layer scope (C1, C2, C4).
Namespace and hence F4's file-scope verdict: fixed by [R-RDR-01], not by L23's cell (C3).
Appenders: byte-identical output where a commit is available, refusal under both where it is not
(C5–C8). Compactors: refusal under both (C9). Writers: emittable set fixed by a pure predicate
on bytes (C10). Corpus: unchanged (C11).

The finding is real as a defect — the Detected cell states a deadline looser than the obligation
§19.1 step 4 actually imposes on the name instance, and L3/L5/L6, the other layer-record *name*
rows, all read "open" — but it is register bookkeeping. It does not change which byte sequences
a conforming implementation may emit, or must accept or reject.
