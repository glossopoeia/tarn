## Findings

### BYTE-LEVEL AMBIGUITY — the pre-trailer pad's content: mandatory zero, or unconstrained slack

**Location.** §6.2 `[R-CNT-05]`, §9.2 `[R-LIF-02]` step 5, §22.3 `[R-SEC-04]` versus §5.2 `[R-CNT-03]`, `[R-CNT-21]`.

**Reading A — the pad MUST be zero, and a nonzero pad fails certification.** `[R-CNT-05]`: "Writers MUST place the directory so that only the **zero** pre-trailer pad — fewer than 64 bytes … — lies between the directory's end and the trailer; a verifier MUST treat **a violation** as a validity error at file scope." The adjective is inside the MUST, so bytes that are not a *zero* pad are a violation. `[R-LIF-02]` step 5 reinforces it: "append the **zero pad** to the next 64-byte boundary." `[R-SEC-04]` (§22.3) states the verifier check outright: "corruption confined to padding is invisible to a reader and caught only by **a verifier's zero check** (`[R-CNT-03]`)." Appendix H lists "declared-padding content (§5.2)" among the checks readers are exempt from and verifiers owe, and Appendix G calls it "already mandatory: zero declared gaps (`[R-CNT-03]`)."

**Reading B — the pad is slack, its content is unconstrained, and zeroing is advice.** `[R-CNT-03]`: "Writers **SHOULD** zero the gaps they create — the run before an aligned tile or slab run, and the pre-trailer pad. … **no conformance requirement rides on slack content either way**." `[R-CNT-21]`: the pre-trailer pad is slack, and "its content is unconstrained, and **no conformance requirement applies to it**." §21.6 lists "the pre-trailer pad" under "Bytes the live state does not claim … Slack: unconstrained content, no conformance requirement." On this reading `[R-CNT-05]`'s "violation" is the *placement* violation the register encodes — F10 and F11 both require that "a **structure**" occupy the gap — and stale bytes are not a structure.

**Discriminator.** Appendix A's 128-byte minimal file with bytes [20, 64) changed from `00` to `AA`. No checksum covers those bytes (§8.1 assigns them none), so the directory CRC at [16,20) and the trailer CRC `D2 38 09 E0` both still verify and every gate of `[R-CNT-06]` still passes.
- Verifier A: reject-file; refuses to certify (`[R-CNT-05]`, `[R-SEC-04]`, Appendix H).
- Verifier B: certifies the file as conforming and reports slack = 44 bytes (`[R-CNT-03]`, `[R-CNT-21]`, §21.6).

It also splits writers: given identical input, a writer reading `[R-CNT-03]` may reuse a dirty buffer for the pad, a writer reading `[R-CNT-05]`/`[R-LIF-02]` step 5 must zero it — different bytes, both claiming conformance.

**What I searched to refute it.** Every occurrence of *pad*, *padding*, *pre-trailer*, *slack*, and *zero* in the document: §5.1 (which still lists "declared padding" as a structure of every generation), §5.2 `[R-CNT-03]`/`[R-CNT-21]`, §6.2 `[R-CNT-05]`, §9.2 `[R-LIF-02]`, §14.5's closing Note, §16.1 `[R-SLB-01]`, §16.2 `[R-SLB-03]`, §20.2 `[R-WRT-02]`, §21.6, §22.3 `[R-SEC-04]`, Appendix A's annotation, Appendix G, Appendix H. The strongest resolving sentence is §14.5's "writers zero it by advice, and no conformance requirement constrains its content" — but that sentence is inside a block labeled **Note**, which `[R-CNF-01]` makes non-normative. §21.1's tiebreak ("where a row and the rule it cites diverge, the rule governs") does not help either: the conflict is rule-versus-rule, both sides carrying MUST, not rule-versus-restatement.

### BYTE-LEVEL AMBIGUITY — which readers are "local", and therefore owe the front-block check

**Location.** §6.1 `[R-CNT-04]`, with §19.1 step 1 `[R-RDR-01]` and §19.2 `[R-RDR-02]`.

`[R-CNT-04]` defines the class by transport behavior, not by storage medium: "A **local reader** — one whose transport delivers the file's bytes from offset 0 without a separate request, as against a **remote reader** fetching byte ranges (§6.4) — … MUST verify the full block by byte equality before other processing and MUST treat any mismatch as reject-file; a remote reader MAY defer or omit this check."

**Reading A.** A reader of a file on local storage is a local reader and MUST reject a file whose front block is wrong.

**Reading B.** A reader that opens the file and issues `pread`/seek+read for the ranges it wants does *not* have a transport that "delivers the file's bytes from offset 0 without a separate request" — it fetches byte ranges, which is exactly how §6.4 characterizes a remote reader. It is therefore a remote reader and MAY omit the check, even on a local disk. Under Reading B the MUST is vacuous, since every reader chooses its own I/O strategy.

**Discriminator.** Appendix A's 128-byte file with bytes [0,8) written byte-reversed as `1A 0A 0D 4E 52 41 54 89` (the exact instance §21.2 row F2 names, and precisely the transport corruption §6.1's Rationale says the signature exists to catch). Nothing else changes; the trailer and directory CRCs are unaffected.
- mmap/whole-read reader: reject-file.
- pread-based reader on the same local file: opens successfully, reports zero layers, returns no error.

Both are defensible as conforming, on identical bytes, with no test in the document to decide which class either belongs to.

**Aggravating cross-reference.** §21.2 row F2 assigns this condition detector **reader** (unqualified) and outcome **reject-file**, and `[R-ERR-02]` requires "one vector per instance" — so the corpus must contain a vector whose expected verdict is reject-file for a byte-reversed front block, which a conforming remote reader fails. §24's note only forgives a reader that rejects *more* broadly than the vector expects, not one that accepts. `[R-VEC-02]` itself says a vector whose expectation cannot be stated in its terms "makes it a finding against this document rather than a vector."

**What I searched to refute it.** Every occurrence of *local reader*, *remote reader*, *sniffer*, *front signature*, and *transport*: §6.1, §6.4 `[R-CNT-09]`/`[R-CNT-10]`, §19.1 step 1, §19.2's tier list, §21.2 rows F2 and F7, §21.6, Appendix A's closing paragraph, Appendix H's conforming-reader checklist. §19.2 preserves the exemption verbatim ("at open: the front signature block (**local readers**, `[R-CNT-04]`)") rather than narrowing it, and Appendix H's checklist omits the front block entirely. Nothing anywhere ties "local" to local storage or forbids a local-filesystem reader from classifying itself by its range-fetching transport.

### CONTRADICTION — §2.3 declares four conformance classes and then defines five

§2.3: "Conformance is defined for **four** classes." The bullets that follow define five: conforming TARN file `[R-CNF-02]`, conforming reader `[R-CNF-03]`/`[R-CNF-04]`, conforming writer `[R-CNF-05]`, conforming updater `[R-CNF-06]`, conforming verifier `[R-CNF-11]`. Appendix H likewise carries five checklists. The out-of-sequence identifier `[R-CNF-11]` on the verifier bullet, sitting after `[R-CNF-06]`…`[R-CNF-10]`, suggests the class was added without updating the count. Not byte-level (no reading changes any byte or verdict), but §2.3 is the section every later section cites for its actor vocabulary.

### CONTRADICTION — §21.6 files two conditions it calls nonconforming under "Conditions that are not violations", against `[R-CNF-07]` and `[R-CNF-12]`

`[R-CNF-07]` (§2.4): "**Every** detectable violation named by this specification is assigned exactly one reader outcome: reject-file, reject-layer, reject-tile, or ignore-record." `[R-CNF-12]` (§2.4): "a verifier certifies only violation-free files."

§21.6 is headed "Conditions that are **not** violations. These are defined behaviors, **not errors**. A reader that treats any of them as a failure is the nonconforming party." Two of its rows contradict their own heading in their own text:
- "A registered record type's stored MU or PE bit differs from the value §7.3's registry fixes | **The file is nonconforming**, but readers apply the type's fixed semantics regardless … a verifier SHOULD report the mismatch | `[R-CNT-22]`" — matching §7.3 `[R-CNT-22]`: "A stored-flag mismatch on a registered type makes the file nonconforming (`[R-CNF-05]`)."
- "A user-metadata document's object members are not sorted … | **The file is nonconforming**, but the document is readable | `[R-MTA-05]`."

Both are detectable violations carrying no reader outcome from `[R-CNF-07]`'s four-value vocabulary and only a SHOULD-report for verifiers, while `[R-CNF-12]` bars certifying them. A verifier reading `[R-CNT-22]` + `[R-CNF-12]` withholds certification from a file whose layer record stores `flags = 00 00`; a verifier reading §21.6's heading and the register's normative completeness claim (§21.1) certifies it. I stop short of calling this byte-level because each row's own sentence says "The file is nonconforming," which a careful reader takes over the heading — but §2.4's "every … exactly one" is then simply false.

### OBSERVATION — "declared padding" survives as a term §5.2 no longer defines

§5.1 lists "declared padding" among the structures lying between the front block and the trailer, but §5.2 `[R-CNT-02]`'s partition offers no class for it (front signature block; stored-tile extent; record extent; directory; trailer), no field anywhere declares padding, and `[R-CNT-21]` folds every such byte into slack. §22.3 `[R-SEC-04]` and Appendix H nonetheless still speak of "Declared padding" and "declared-padding content (§5.2)". Same residue as the first byte-level finding above.

### OBSERVATION — §9.7's coverage walk never reaches the front block or the trailer, yet declares everything unreached to be slack

`[R-LIF-08]`: "From the live trailer it enumerates the live directory and its records, each record's extent, and each layer's tile-index region together with that region's non-sentinel entries; it checks that these occupy disjoint byte ranges, that each lies within [16, F − 64) … **Bytes the walk does not reach are slack**: the verifier sums them and reports the total." The enumeration omits the front signature block and the trailer, both of which §5.2 lists as coverage classes of the live committed state. A verifier implementing §9.7 literally reports 80 extra slack bytes on every file — on Appendix A's minimal file, 124 instead of 44 — and `[R-CNT-21]` makes reporting that total a MUST. §5.2 resolves it, but §9.7's walk should name both structures explicitly, and the `[16, F − 64)` containment bound needs the trailer excluded.

### OBSERVATION — register-completeness gaps against §21.1's normative completeness claim

§21.1: "Its **completeness is normative** — a violation this specification names and the register omits is a defect in this document." Violations named in §5–§7 with no §21.2/§21.3 row:
- A front-signature-block mismatch other than byte-reversal — e.g. the reserved bytes [8,16) nonzero, which `[R-CNT-04]` and §6.1's layout table make reject-file. F2 covers only the byte-reversed case, and only bytes [0,8).
- A user-metadata record whose `extent_length` is 1–4 — `[R-CNT-25]` makes this "a validity error at its containing scope"; F26 and L11 cover only extent slot (0, 0).
- A user-metadata record whose `inline_length` ≠ 1 — `[R-MTA-03]`, "a validity error at the record's containing scope."
- `[R-CNT-05]`'s under-64-byte gap bound violated by pure slack: F10 and F11 both require that "a **structure**" occupy the gap, so a 236-byte all-slack gap between directory end and trailer matches no row.
- `[R-LIF-03]`'s "increasing by exactly 1 per commit" has no row (arguably undecidable from the live state by §9.7's design, in which case §21.7 should say so).

### OBSERVATION — duplicate register rows and an off-by-one instance count

§21.2 carries three duplicate or near-duplicate pairs: F8 ≡ F9 verbatim, F10/F11 differing only by the words "other than the zero pre-trailer pad", F34 ≡ F35 verbatim (including their identical seven-instance lists). Each pair inflates the "37 conditions" header, `[R-ERR-02]`'s "120 conditions", and — through `[R-ERR-02]`'s one-vector-per-instance rule — forces 16 duplicate conformance vectors from F34/F35 alone. Separately, counting instances mechanically by §21.1's stated rule (semicolon-separated items; a cell reading "—" is one) yields 69 + 81 + 43 + 20 = **213**, not the 214 §21.8 states; §21.3 also skips row identifier **L40** with no withdrawal note, unlike §14.4's explicit retirement of `[R-SER-04]`. The pattern is consistent with L40 having been deleted and the condition counts updated (48→47, 121→120) while the instance total was not (214→213).

### OBSERVATION — `file_id` needs an explicit exemption from `[R-ENC-03]`

§6.2's table bounds `file_id` only by "≠ 0", and `[R-ENC-03]` scopes its 2⁶³ − 1 ceiling to "every offset, length, extent, and count" — repeated identically in §21.9 `[R-ERR-05]` and Appendix B — none of which `file_id` is. That is the right reading, and it must be: §9.3 `[R-LIF-03]` says the creating writer "SHOULD draw it from a cryptographically random source," and a random `u64` exceeds 2⁶³ − 1 half the time, so an implementer who applied `[R-ENC-03]` to it would reject-file on half of all correctly created files. One sentence saying `file_id` is not subject to `[R-ENC-03]` would close it. Adjacent asymmetry: §6.2's table *does* bound `generation` at 2⁶³ − 1 citing `[R-ENC-03]`, but `[R-CNT-06]`'s enumerated gate list says only "generation ≥ 1", and F3's instance list omits `generation` — so the upper bound on generation has no reader gate and no register row.

### OBSERVATION — `[R-ENC-12]` lacks the metadata carve-out `[R-ENC-11]` carries

`[R-ENC-11]` ends "— except inside a user-metadata document, where `[R-CNT-25]`'s quarantine governs and the outcome is ignore-record." `[R-ENC-12]`, which governs the same strings when they are user-metadata *keys* ("the strings that identify layers, dimensions, channels, and user-metadata keys"), says flatly "a reader MUST treat such a name as a validity error at the owning scope" — reject-file for a top-level document. `[R-CNT-25]`, `[R-MTA-04]`, and register rows R5/R9 resolve it to ignore-record, but the asymmetry between two adjacent requirements about the same strings invites the wrong outcome.

### OBSERVATION — the metadata-encoding space lacks the conforming/nonconforming split `[R-CNT-15]` draws for record types

For record types, `[R-CNT-15]` states it explicitly: an experimental-range value is **conforming** ("§10.3's prohibition binds the writer's conduct, not the bytes, `[R-CNF-02]`"), a reserved-range value is a violation a verifier MUST flag. The same split follows for §18.2's metadata encoding — §18.2 has no flat "writers MUST NOT emit" (unlike §11.4, §12.2, §14.1, §17.2, §17.3), so `[R-CNF-02]`'s conduct carve-out, which names §10.3 by number, leaves an experimental encoding byte ≥ 0x80 conforming while a reserved 3–0x7F is not. Register row R1 lumps both as "any value other than 1 (none) or 2 (zstd)" with no conformance distinction, and Appendix H's file checklist ("no violation row of §21.2–§21.5 applies") then reads both as nonconforming. Stating the split in §18.2 as §7.2 states it would remove the need to reconstruct it from `[R-CNF-02]`.

### OBSERVATION — smaller citation and enumeration slips

- §21.2 row F7 cites `[R-CNT-01]` as the governing rule for the 128-byte minimum; the rule is `[R-CNT-27]`.
- §4.5 enumerates the interior checksum fields as "each segment CRC array and each layer record's `crc_of_crc_array`", omitting a tile-index entry's `crc` field, which is equally comparison-verified and covered by exactly one further checksum (its segment CRC, §8.1). The general rule holds; the list is short one member.
- Appendix G's closing line calls `[R-CNT-03]` "already mandatory"; `[R-CNT-03]` is a SHOULD.

## Verdict
BYTE-LEVEL AMBIGUITIES: 2
CONFIDENCE: high
