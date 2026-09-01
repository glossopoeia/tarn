# Refute-only verification — §21.5 experimental-encoding exception read over [R-CNT-25]'s full list

Verdict: **NOT_BYTE_LEVEL**

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
Sections opened in it: §2.1, §2.2, §2.3, §2.4, §7.1, §7.2, §7.3, §8.1, §8.2, §9.7,
§10.1, §10.2, §10.3, §10.4 (through [R-EXT-05]), §18.1, §18.2, §19.1, §19.2, §19.3,
§20.4, §20.5, §21.1, §21.4 tail, §21.5, §21.6, §21.7, §21.8, §21.9, §22.3, Appendix H.

Ran: `wc -l`, `grep -n` and `sed -n` against that one file only; one `python3 -c`
inline script computing CRC-32C (Castagnoli, reflected, poly 0x82F63B78) over
three literal byte strings — it read no file. Scratch directory created at
`.../r28-refute/priv-experimental-encoding-exception-over-broad/` (nothing written
into it; the CRC script was an inline `-c`).

No ADRs, no `docs/`, no `conformance/`, no `registry.json`, no git history, no
directory listing, no web.

Injected context that appeared before I began, and which I disregarded: a
`claudeMd` block pointing at AGENTS.md, a `userEmail` line, a `currentDate` line,
and an environment block naming the repository, the branch, git status and five
recent commit subject lines. None of it is specification text and none of it
entered the analysis. Also present: an MCP-server instruction block and a
deferred-tool listing, likewise irrelevant.

## The question

BROAD: §21.5's exception ranges over the whole set [R-CNT-25] enumerates — whose
first member is "a failed extent CRC" — so at a metadata encoding ≥ 0x80 a failed
user-metadata extent CRC is not a violation, R2 does not apply, the file is
conforming, and a verifier certifies.

NARROW: the exception is bounded by its own stated ground, "where no *document
rule* attaches". The extent's terminal CRC is not a document rule; R2 survives at
every encoding; such a file is nonconforming.

If BROAD were permitted this would be byte-level, and it is worth saying plainly
rather than burying: the disputed file is a *conforming* file under BROAD. That is
the exact pattern this project's discriminator marks as a real fork, not the
[R-CNF-05]-bars-it-anyway pattern. So the whole case turns on one hinge.

## Constructions attempted

**C1 — minimal verifier accept/reject fork.** File with zero layers (§21.6: "The
file contains zero layers | A conforming file with an empty directory"), one
top-level user-metadata record, type 0x0002, MU=0/PE=1, inline_length 1, encoding
byte 0x80, extent_length 5 — the floor F22 sets. Extent = `7B` (`{`) followed by
four bytes. CRC-32C(`{`) = 0xBA6CAC67, stored little-endian as `67 AC 6C BA`.
Store `00 00 00 00` instead: the terminal 4 bytes do not equal the CRC-32C of the
preceding byte, and R2's condition holds on its face. Verifier A (BROAD)
certifies; verifier B (NARROW) reports nonconforming. Correspondingly a writer
under BROAD may emit those four bytes and under NARROW may not — a 4-byte
difference at extent_offset+1.

Killed. Four independent normative passages close BROAD:

1. [R-MTA-10], the rule the exception itself cites, in an express closed list that
   puts the CRC on the conformance side: "no content rule attaches to the extent's
   bytes, and file conformance — a pure predicate on bytes (`[R-CNF-02]`) — is
   decided by the structural checks that precede the document alone: the record's
   framing and extent slot (`[R-CNT-13]`), the encoding byte's own value set
   (`[R-MTA-03]`), and the extent's terminal CRC (`[R-CNT-20]`)." The same
   sentence names what *is* withdrawn, and it is a closed enumeration: "The
   document rules of this section — the frame constraints of encoding 2, the
   decoded-document restrictions above, and `[R-MTA-05]`'s member ordering".
2. §19.2 [R-RDR-02], which none of the three triage passes cited, and which is the
   cleanest of the four because it sets the CRC and the content rules side by side
   and attaches the encoding qualifier to one of them only: "**at use of a
   record's extent:** that extent's CRC and the content rules of the document it
   carries — those §18.2 attaches at its encoding (`[R-MTA-10]`) — before anything
   the extent holds is returned". The restrictive clause "those §18.2 attaches at
   its encoding" modifies "the content rules", not "that extent's CRC".
3. §8.1's map, unqualified by encoding and expressly stated to be pre-decode:
   "| User-metadata extent | final 4 bytes of the extent | the preceding bytes
   (the encoded bytes exactly as stored, before decoding) |" — and note the
   drafters *did* write an encoding-blind exemption one row down, for a different
   thing: "| Extent of a record of a type this specification has not assigned |
   none — the bytes are opaque |". Unassigned *type*, not unassigned *encoding*.
   §9.7 [R-LIF-08] then makes the walk check it — "each verifies against the
   checksum covering it, where §8.1's map states one" — and in the very next
   sentence says exactly how far the withdrawal reaches: "A user-metadata document
   under an unassigned encoding asks nothing of this walk: no rule attaches to its
   *content*".
4. §22.3 [R-SEC-04]: "the extent of a user-metadata record under an unassigned
   encoding is covered by its terminal CRC but constrained by no content rule".

And the preamble's own next sentence states the limiting principle in general
terms, not as a one-off carve-back for R1: "what `[R-MTA-10]` withdraws is the
document's content rules, never the encoding byte's own value set". A failed
extent CRC is not a document content rule.

**C2 — writer emittable set, taken on its own.** Same construction from the
writer's side: [R-CNF-05] bars a conforming writer from emitting a nonconforming
file, so under NARROW no conforming writer may emit C1's file and under BROAD one
may. Killed by the same hinge as C1: the file is nonconforming under the only
permitted reading, so both readings bar it and the emittable set does not move.

**C3 — compaction path.** Compactor relocating that extent. Hoped for: BROAD
carries it forward, NARROW refuses. Killed *independently of the hinge*, which
makes it the one construction that would have failed even if BROAD were
permitted. [R-WRT-09] fixes a compactor's verification depth as "each relocated
extent's checksum" — an obligation phrased over §8.1's map, not over violation
status — and [R-WRT-06] then says "A compactor MUST refuse to compact when any
check `[R-WRT-09]` obliges fails". Both readings refuse; no output file exists
under either, so no byte differs.

**C4 — append path, byte-identical re-emission.** Appender retaining the record
under [R-WRT-05] ("MUST re-emit byte-identically — header, inline payload, and
extent slot — every record it retains and does not logically modify"), the extent
unmoved in the committed prefix. §20.4 forbids dropping it ("No commit therefore
removes a layer record, or a user-metadata record at either scope"), so under
NARROW the updater cannot produce a conforming output without minting a fresh
extent, while under BROAD it re-emits and commits. Killed by the same hinge as C1;
this is C1 wearing a different hat, not an independent path.

**C5 — reader behavior.** Does any byte a reader *returns* differ? No. Both
readings give ignore-record — [R-CNT-20] ("a user-metadata extent's CRC →
ignore-record") and §21.6's entry ("Ignored (ignore-record)") agree on the
outcome — and §2.4 defines it identically in both: "The record is skipped as
though absent. Decoding of all stored data is unaffected." Only the diagnostic
would differ, and [R-CNT-25]'s report obligation is a SHOULD, which [R-CNF-12]
places outside the register entirely.

**C6 — degenerate extent.** extent_length exactly 5, the floor F22 sets: one
document byte plus four CRC bytes. CRC-32C over a single byte is well defined
(CRC-32C(`\x00`) = 0x527D5351), so nothing degenerates and neither reading
changes shape. Killed.

**C7 — the extent already what the rule would set it to.** If the stored terminal
4 bytes happen to equal the CRC, R2's condition is false and the two readings
coincide trivially. Killed.

**C8 — a third verdict rather than a second.** Could BROAD instead produce
*cannot establish*, forking the verdict that way? Expressly foreclosed in §2.3
[R-CNF-11]: "A user-metadata document under an encoding this specification does
not assign is not such a ground: no content rule attaches there, so nothing is
left unchecked, and certification is unaffected". And "An established violation
takes priority". Killed.

**C9 — layer sub-record instead of top-level.** [R-CNT-25]'s quarantine is
"whatever the containing scope" and §21.1 repeats it for every §21.5 row, so the
sub-record instance analyses identically. Killed.

**C10 — encoding 0 or a reserved value instead of experimental.** [R-MTA-10] is
written over "an unassigned encoding" generally, which covers 0 and the reserved
range, so the CRC survives there too; the preamble expressly keeps R1 alive there.
No fork. Killed.

**C11 — Appendix H, which contains the BROAD-sounding sentence.** "a user-metadata
record at an experimental-range encoding is no violation and no bar, and is
instead reported: owning scope, encoding value, stored extent length
(`[R-MTA-10]`)". Killed twice over. First on the label, which discriminator #3
tells me to check before relying on non-normativity: the heading reads "Appendix H
— Conformance checklists (non-normative)", and [R-CNF-01] exempts "appendices
identified as non-normative". Second on its own terms — the appendix says "each
entry's authority is the requirement or section cited, never this summary", it
cites [R-MTA-10], and its own Conforming-file bullet reads "every structure's
checksum verifies where §8.1's map states one".

**C12 — §21.6's entry as an immunity.** "the file is conforming ... a verifier
certifies, reporting the record it ignored". Killed on §21.1's express clause,
which reaches §21.6 by name: "§21.6's entries restate their governing rules on the
same terms a row does, and where such an entry and the rule it cites diverge, the
rule governs there too." The entry cites [R-MTA-10]. Killed a second time on
parity: every §21.6 entry says a *condition* is not a violation, never that a file
exhibiting it has no others — "version_minor is higher ... | Accepted" does not
save a file with a broken trailer CRC either. §21.6's own preamble is written over
conditions: "These are defined behaviors, not errors."

**C13 — the skeptic's residual worry, that §21.1's precedence clause is written
about rows and §21.6 entries and not about §21.5 preamble prose.** I went looking
for whether that leaves the preamble as a free-standing second authority. It does
not. [R-EXT-05] states the principle generally and names §21 as an instance:
"Where the registry, §10.2's table, and Appendix C diverge, the section that
defines the space governs — the registry is machine-readable convenience, never a
second authority (§21.1 applies the same principle to the error register)." §18.2
is the section that defines the metadata-encoding space (§10.2's table: "metadata
encoding (§18.2)"). Independently, the §21.5 preamble carries no requirement
identifier of its own while [R-MTA-10] does, and §2.2 attaches identifiers to
"Normative requirements". And independently again, R2 *is* a row, its Governing
rule cell is `[R-CNT-20]` (not [R-CNT-25]), and §21.1 says "where a row and the
rule it cites diverge, the rule governs" — [R-CNT-20] states the failed
user-metadata extent CRC with no encoding qualifier at all.

## Conclusion

Every path to a fork runs through one hinge — whether BROAD is a permitted
reading — and BROAD is closed by [R-MTA-10]'s express closed list, by §19.2's
side-by-side listing where the encoding qualifier restrictively modifies the
content rules alone, by §8.1's encoding-blind map row read with §9.7's "no rule
attaches to its *content*", and by §22.3. The one construction that does not run
through the hinge (C3, compaction) dies on [R-WRT-09]/[R-WRT-06] under both
readings.

The defect the reporters found is real and the drafting hazard is real — the
sentence's exception is written over a set whose first member the exception does
not mean to reach, and its correction lives three sections away. But it does not
move the set of byte sequences a conforming implementation may emit, or must
accept or reject.
