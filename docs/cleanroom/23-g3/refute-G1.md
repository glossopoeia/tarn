# G1 refute-only working transcript — finding A-03

## 0. Disclosure of unrequested context

Before my first action, my runtime placed material in context: a project
instruction file pointer (CLAUDE.md, which only redirects to AGENTS.md) and an
index of the maintainer's personal memory notes with short one-line
descriptions. I did not open AGENTS.md, and I did not open any of the memory
files the index names. I am naming that this appeared, not repeating its
contents, and no conclusion below rests on it. Nothing in it was about
Window_Size, §18.2, or [R-COD-06].

## 1. What I read and ran

Read in full:
- /private/tmp/.../r23audit/refute/finding-A-03.md
- /private/tmp/.../r23audit/hunk-01.diff

Read from spec/tarn.md (by `sed -n`, absolute path
/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md):
- lines 2225-2300  (§17.2 codecs 1-4, all of [R-COD-06] and the two Notes)
- lines 2430-2520  (§18.2 from [R-MTA-02] through the [R-MTA-09] paragraph and
                    the 16 MiB Note)
- lines 250-275    ([R-CNF-12] and the head of §2.5)
- lines 3660-3720  (§21.8 [R-ERR-02], §21.9 [R-ERR-03], the guarantees table,
                    the per-instance scope paragraph, [R-ERR-04])
- lines 3536-3550  (§21.5 preamble tail and rows R1-R8, including R4)
- lines 4080-4110  (Appendix B constants table, incl. the §21.9 restatement row)
- lines 4193-4260  (Appendix G, "Reproducible-writer profile (non-normative)")

Greps run (all against spec/tarn.md only) and their exact yields:

    grep -n "Window_Size" spec/tarn.md
    2293, 2298, 2300, 2461, 2470, 3690        (6 hits)

    grep -n "R-ERR-03\|R-ERR-04" spec/tarn.md
    163, 201, 2296, 2477, 2509, 3679, 3715, 4353

    grep -n "R-COD-06" spec/tarn.md
    2296, 2458, 2486, 3505, 3509, 3510, 3511, 3512, 3513, 3514, 3546, 3614, 3777

    grep -ni "Writers SHOULD\|writer SHOULD\|SHOULD keep" spec/tarn.md
    498, 660, 820, 836, 1226, 2157, 2292, 2620, 3032, 4095

    grep -n "declared window\|frame's declared\|window bound" spec/tarn.md
    2293, 2461, 2470, 2472, 3531

    grep -n "Appendix G" spec/tarn.md
    663, 1861, 2264, 4193

Note on the hard wrap: I deliberately searched only short fragments that cannot
straddle a line break — `Window_Size` (backticked, one token), `R-COD-06`,
`declared window`, `window bound`, `Appendix G`. The one multi-word search that
could have wrapped (`Writers SHOULD`) is confirmed by its hit at 2292, where the
wrap falls immediately after it ("Writers SHOULD keep the / declared window"),
so the pattern is demonstrably able to match in this file. No conclusion below
rests on a failed grep alone.

## 2. The charter's task: enumerate the excepted rule, check each part

§18.2, lines 2456-2462 (normative prose, no blockquote, paragraph ends
`[R-MTA-09]`):

> Encoding 2 stores it as exactly one RFC 8878 compressed frame occupying the
> extent's bytes before its terminal CRC, under every frame constraint
> `[R-COD-06]` places on a frame, named here or not, save two: what it states
> against a tile's declared decoded size, and what it states about the frame's
> declared `Window_Size`. This section replaces both, below.

Full enumeration of what [R-COD-06] (lines 2270-2296) states inside the two
excepted headings:

Heading A — "against a tile's declared decoded size":
  A1. "MUST NOT declare a window size exceeding the tile's decoded size"
      (also inside heading B — the overlap the auditor flags).
  A2. "a reader MUST treat either as a validity error at tile scope"
      (the "either" distributes over the checksum flag and A1; only the A1
      prong is excepted).
  A3. "The frame content-size field MAY be present; when present it MUST
      equal the tile's decoded size, a reader MUST treat a mismatch as a
      validity error at tile scope"
  A4. "and a reader MUST NOT allocate or size any buffer from it — the decoded
      size comes from the layer's declarations alone (§14, `[R-SER-07]`)"
      (borderline: same sentence as A3, but its subject is the frame's
      content-size field, not the tile's decoded size).

Heading B — "about the frame's declared `Window_Size`":
  B1. = A1, the MUST NOT.
  B2. = the A1 prong of A2, the reader's tile-scope validity error.
  B3. "Writers SHOULD keep the declared window within §21.9's 8 MiB
      `Window_Size` guarantee even for a larger tile"
  B4. "a wider window is conforming and merely permits a conforming reader to
      decline the tile or the layer on resource grounds (`[R-ERR-04]`)"

Replacements actually present in §18.2 (all in normative prose, none in a
blockquote — I checked line-start characters; the only `>` lines in the passage
are the 16 MiB Note at 2504-2513, which I did not rely on):

  A1/B1, A2/B2  -> line 2470-2477: "The frame's declared `Window_Size` is
      unconstrained here for the same reason, and takes the same treatment: a
      reader's window bound is its own, no smaller than §21.9's guarantee for
      that quantity, and a frame declaring more than the reader admits is
      ignore-record on that ground ... and no violation".
      Withdrawal of the MUST NOT plus a stated substitute disposition. Replaced.
  A3   -> lines 2478-2487: content-size "MAY be present, and when present it
      MUST equal the byte length of the decoded document", routed to R4.
      Replaced.
  A4   -> line 2448-2449 carry-over: "the bar on sizing any buffer from a
      length the frame itself declares". Restated, so covered whichever
      heading one assigns it to.
  B4   -> line 2476-2477: "the file exceeds a §21.9 guarantee and so remains
      conforming while the reader MAY decline it (`[R-ERR-04]`)". Replaced.
  B3   -> NOTHING. Confirmed by the grep at §1: `Window_Size` appears in only
      six places in the whole document, and the two inside §18.2 (2461, 2470)
      are the exception clause and the reader-side treatment. `declared window`
      appears at 2293 ([R-COD-06], the excepted SHOULD) and nowhere in §18.2.
      There is no writer-directed window guidance anywhere in §18.2.

So the auditor's textual claim is CORRECT on its face: "This section replaces
both" is written over an excepted body of text one of whose four parts (B3) has
no counterpart in the section. The verifier's point 1 — that "unconstrained
here" positively disposes of B3 — is a reading, not a quotation. "Unconstrained"
disposes of constraints; a hortatory SHOULD is not a constraint, which is
exactly [R-CNF-12]'s own distinction. I do not accept point 1 as stated.

That said, the question I am asked is not whether point 1 is well-argued. It is
whether the gap moves bytes.

## 3. Constructions tried

### C1 — Emittable set, writer, metadata path
Writer emits a user-metadata record, encoding 2, document decoding to 12 MiB,
frame header declaring Window_Size = 64 MiB.
- Reading X (auditor's: B3 excepted and unreplaced): file conforming, nothing
  advises against it.
- Reading Y (verifier's: B3 disposed by "unconstrained here"): file conforming,
  nothing advises against it.
Identical. And even a third reading Z, in which B3 is *imported* through "every
frame constraint ... named here or not" (arguing a SHOULD is not a
"constraint"), still yields a conforming file, because [R-CNF-12] lines 260-263:
"Deviation from a SHOULD is not a violation for this purpose: §21's register
enumerates MUST-level conditions only". Three readings, one emittable set.
NOT byte-level.

### C2 — Accept/reject, reader
Same file. §21.9's 8 MiB row is per-instance and its scope paragraph (lines
3697-3701) says "The other two range over the user-metadata documents and
compressed frames a file actually contains" — a metadata encoding-2 frame is a
compressed frame the file contains, so the row covers it. 64 MiB exceeds the
row, so [R-CNF-03]'s acceptance duty (as [R-ERR-03] frames it: "a conforming
reader MUST accept any conforming file whose quantities lie within these
bounds") does not attach, and [R-ERR-04] licenses a decline; §18.2 independently
makes it ignore-record against the reader's own bound. All of this is untouched
by B3, which is addressed to writers. Every reading: same accept/reject.
NOT byte-level.

I checked the one way this could have gone the other way: if the 8 MiB row did
NOT range over metadata frames, then a 64 MiB metadata window would be a
quantity within all bounds, [R-CNF-03] would compel acceptance, and §18.2's
ignore-record licence would contradict it — a genuine accept/reject split. The
scope paragraph at 3697-3701 forecloses it. So that route is closed.

### C3 — Verifier
[R-CNF-12] lines 262-266: "a verifier reports a SHOULD deviation as an advisory
that does not bar certification. A verifier owes no search for one". Certifi-
cation verdict identical under all three readings. NOT byte-level.

### C4 — Register / corpus
§21.8 [R-ERR-02] requires a vector per row and per instance of §21.2-§21.5.
[R-CNF-12] confines the register to MUST-level conditions, so B3 generates no
row and no vector. §21.4's T21 keeps the tile-side MUST NOT (line 3513) and R4's
instance list (line 3546) contains no window instance — exactly what a withdrawn
window constraint predicts. The register is consistent with the repair.
NOT byte-level.

### C5 — Actor enumeration (the charter's second suggested move)
Actors this document defines: writer/creator, compactor, reader, verifier.
Compactor: re-encoding a metadata document, its window choice is free under
every reading (nothing in §18.2 or [R-COD-06] constrains it, and [R-WRT-06] is
about file_id). Reader and verifier: covered in C2/C3. No actor's emitted bytes
turn on B3.

### C6 — Is there a hidden MUST that elevates the SHOULD?
Grep of all ten "writer SHOULD"/"Writers SHOULD"/"SHOULD keep" hits: 498 (NFC
names), 660 (zero gaps), 820 (lowest version_minor), 836 (dir_length discovery
window), 1226 (random file_id), 2157 (zero sentinel bytes), 2292 (the excepted
one), 2620 (standardized key scopes), 3032 (produce instead of...), 4095
(Appendix B row for the §6.4 discovery window). None is a general obligation to
stay inside §21.9 guarantees, and none reaches metadata frame windows.
Appendix G, the one place a SHOULD could be hardened into byte-exactness, is
headed "Reproducible-writer profile (non-normative)" (line 4193) and says of
itself "It adds no requirement to any actor: a writer ignoring it is fully
conforming" — and its item 1 states byte-identity across implementations "is
therefore unattainable for codecs 2-4". So no profile makes the window
determinate. NOT byte-level.

### C7 — The "save two is not a partition" sub-claim
A1 = B1: the window MUST NOT satisfies both headings. Tested for
UNDER-coverage under every partition a reader might draw:
  - A covers {A1,A3,A4}, B covers {B3,B4}: union excludes A1,A3,A4,B3,B4.
  - A covers {A3,A4}, B covers {B1,B2,B3,B4}: union excludes the same set.
Either way nothing MUST-level falls outside the union, and §18.2 supplies a
treatment for each excluded MUST-level part (C2 above). Tested for
OVER-coverage: could heading A drag out something §18.2 fails to restate? A4 is
the only candidate, and §18.2 restates it verbatim in the carry-over list.
Harmless, as the auditor conceded. NOT byte-level.

### C8 — The charter's first suggested move ("nonconforming anyway" premise)
This move does not apply here, because the downgrade does not rest on a
"nonconforming anyway" premise. It rests on "a SHOULD carries no conformance
force", which [R-CNF-12] states in terms, in normative prose outside any
blockquote (lines 260-266). I could find no construction in which the disputed
file's status differs between readings, because under all readings it is
conforming and under all readings a reader may decline it.

## 4. Where the verifier was weak, and why it does not rescue the finding

The verifier's point 1 overclaims: "unconstrained here" is a disposition of
constraints, and B3 is not a constraint, so B3 is genuinely unreplaced and
"replaces both" is genuinely overstated. Point 3 is also slightly off: it says
the pre-repair closed list "excluded it too", which is true, but it uses that to
argue the repair "broke nothing" — the repair did widen the import materially
elsewhere (the carry-over now adds "no dictionary use, disclosed or not", which
the old closed list did not carry). Neither weakness is a byte-level rescue of
A-03, because A-03's own asserted consequence is a writer-side SHOULD, and
[R-CNF-12] settles what a SHOULD is worth.

Points 2 and 4 hold on the text: the writer-side information the auditor says is
absent is present, in [R-ERR-03] ("a writer MAY rely on that", line 3678-3679)
plus [R-ERR-04] ("A file exceeding any of these remains conforming, and a reader
MAY decline it", line 3711-3712), and §18.2 points at the exact row with "no
smaller than §21.9's guarantee for that quantity" (line 2472-2473). A writer
reading only this document knows precisely what staying inside 8 MiB buys and
what exceeding it forfeits. What is missing is encouragement, not information.

## 5. Verdict

A-03 is a real editorial defect — "replaces both" is written across four parts,
one of which is replaced by nothing — and is NOT byte-level under any
construction I could build. The emittable set and every accept/reject verdict
are identical under the auditor's reading, the verifier's reading, and a third
reading in which the SHOULD is imported. DOWNGRADE_STANDS.
