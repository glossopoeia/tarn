# Refute-pass transcript — X-01

## Read
- case/case-X-01.md, hunk-01.diff, hunk-02.diff (charter-permitted)
- spec/tarn.md: 98-115 (R-CNF-01), 1485-1500 (§11.1 Rationale, hunk 01 landing),
  1527-1560 (§11.3), 1700-1745 (§13.1/13.2 fill field), 1880-1935 (§14.3 packed
  planes + pad-bit Note), 1935-1990 (§14.5 R-SER-05), 2985-3060 (§20.3 step 4),
  3345-3375 (§21.1 rule-governs-row), 3495-3560 (§21.4 rows T2/T4/T5/T26),
  3665-3700 (§21.7), 3925-3970 (§23.1, hunk 02 landing)

## Greps (whitespace-normalised with `tr '\n' ' '` because the file is hard-wrapped)
- `already hold` -> 6 hits. Carve-out instances: §11.1 Rationale (no pointer),
  §20.3 x2 (BOTH carry "the fill `[R-SER-05]` fixes"), §23.1 ("the channel's
  recorded fill"). Other 2 hits unrelated (R-CNT-04 resident bytes, §21 F6 note).
- `stored byte already` -> 2 hits: §11.1 Rationale, §20.3 first occurrence.
- `fill bit` -> 5 hits: 1710 (R-TYP-06 "bit-exactly"), 1961+1963 (R-SER-05),
  3538 (T4 instances), 3539 (T5).
- `structurally constrains` -> 1 hit, line 3684.
- `restat` -> §21.1 at 3354 (rows), 3367 (§21.6 entries). No precedence clause
  covering a normative prose restatement such as §23.1's.

## Constructions built and tested

### C1. Auditor's worked case, re-derived independently
rank-1 planar packed bool, C=1, T0=8 so P=8, decoded size ceil(8/8)=1 byte,
P mod 8 = 0 so NO pad bits (§14.3). E0=8 -> G0=1, one addressed tile, stored
0x0B. Shrink E0 -> 5: G0=ceil(5/8)=1 (unchanged), entry_count = C*N = 1
(unchanged), P unchanged so decoded size unchanged, positions 5,6,7 become
padding positions (§11.3). 0x0B = 0b00001011, bits 5,6,7 = 0 = the fill bit for
fill=false. T4 does not fire; T5 has no antecedent (no pad bits). Generation 8
is conforming. So IF a divergence existed it WOULD be byte-level — the
verifier's "byte-level NO" is derivative on its "not real" argument, not
independent. I therefore tested only whether the divergence is real.

### C2. Does the byte-equality reading survive its OWN numeric case?
§13.1: "Every channel entry records a fill value: exactly the channel's element
size in bytes". So for a uint16 channel the recorded fill is TWO bytes. Under
the auditor's Writer-A reading ("the stored byte" == the fill), the carve-out
is inapplicable to every numeric channel of element size > 1, and to every
interleaved position carrying more than one channel. But §20.3 says of the
carve-out "a shrink producing only those is permitted here exactly as it is
there", with no type or layout restriction, and the §14.5 Example's own worked
padding case is uint16. Writer A's reading therefore guts the carve-out for
almost every layer, not just packed bool. That is not a granularity dispute
about packed planes; it is a reading the sentence cannot bear anywhere.

### C3. Would Writer A's comparison even be well-formed?
Writer A compares 0x0B against 0x00. 0x00 is the recorded fill BYTE (§13.2,
bool fill is one byte, 0x00 or 0x01). But §14.3 says a packed plane's byte holds
eight VALUES at bit k mod 8, and T5 tests pad bits against "the channel's fill
bit", never against the fill byte. So Writer A must simultaneously contradict
§14.3, §14.5 and T5 to construct the comparison. A conforming implementation
cannot hold that reading.

### C4. Actor sweep on hunk 02 (§23.1)
Who could be bound by §23.1's clause and not by §20.3?
- writer/appender: §20.3 is the operative permission ("An extent MAY also
  **shrink**"); §23.1's clause is reported speech, explicitly attributed
  ("§20.3 step 4 permits that shrink only where..."). Chasing it lands on §20.3.
- verifier: checks T4/T5, which do not fire in C1.
- reader: §14.3 "padding-position content binds writers, never a reader's
  decode path".
- compactor (§20.5): writes a new file; §20.3's bar is on a commit against a
  superseded generation.
No actor reaches a different verdict via §23.1.

### C5. The auditor's own "contradicting text" reconciles hunk 02
T4's condition cell reads "A padding position does not encode, for each channel
it carries, that channel's **recorded fill value**", and its Instances cell
enumerates "packed planar bool plane fill bit" as one instance of exactly that
term. Hunk 02's phrase is "the channel's recorded fill" — the document's own
umbrella term, of which the fill bit is a listed instance. This is a refutation
of the finding as text for hunk 02, not merely a charge of imprecision.

### C6. Hunk 01 normativity
Line 1483 opens "> **Rationale.** Empty layers serve schema-first workflows".
[R-CNF-01] (line 105-106) excepts Rationale text. The block also names its own
governor ("§20.3 states normatively, and governs"). Additionally the '-' side
of hunk 01 ALREADY lacked the "[R-SER-05] fixes" pointer, so the repair neither
introduced nor worsened the omission. Same for hunk 02: the complained-about
clause ("permits that shrink only where those bytes already hold the channel's
recorded fill, which the layer record publishes") is textually IDENTICAL on
both sides of the diff — the repair only re-flowed it.

### C7. Pad bits vs padding positions — a genuinely different structure
§14.3 Note: "Pad bits are not padding positions (§11.3)". §20.3's bar lists
"the set of padding positions (§11.3) and the content [R-SER-05] fixes there",
which does not name pad bits. I tested whether a shrink can reach a pad bit:
pad bits exist iff P mod 8 != 0 where P = prod(Ti); a shrink changes Ei, never
Ti, so P is invariant and the pad-bit set and content are untouched by any
shrink. No shrink-side gap. (A fill-value re-declaration could reach pad-bit
content with no padding position present, but §20.3's lead clause — "alters ...
what §14 fixes for its stored bytes" — covers it, and that is not X-01.)

### C8. "byte" as the document's container word
§21.7 line 3684-3685: "A change reaching a byte §14 structurally constrains —
a padding position, a pad bit, or a boolean byte — fires §21.4's content rows",
and 3674-3675: "except where §14 constrains a byte's content — a padding
position, a pad bit, or an interleaved boolean". The document explicitly calls a
pad bit — a sub-byte structure — "a byte §14 structurally constrains". I
verified both quotations in situ; the verifier's citation is accurate.

## Where the verifier was loose, and whether it matters
- Its point 3 says "the effect test is satisfied". True, but the effect test is
  reached only through the carve-out, since the shrink DOES alter "the set of
  padding positions". The verifier half-noticed this ("the auditor's literal-list
  reading is self-defeating"). It does not change the outcome: C2/C3 show the
  carve-out reaches the packed case on its own terms.
- Its point 5 calls hunk 02 "granularity-neutral" without citing T4's condition
  cell, which is the sentence that actually proves it. Supplied as C5.

## Residual document gap (non-decisive)
§21.1 states "where a row and the rule it cites diverge, the rule governs" for
§21.4 rows and again for §21.6 entries. There is no analogous clause for a
normative PROSE restatement outside §21, such as §23.1's account of §20.3
step 4. Here it costs nothing because §23.1's wording is the document's own
umbrella term and does not diverge. It is a standing hazard, not an answer to
X-01, and X-01 is fully answered by in-document text.

## Verdict
DOWNGRADE_STANDS.
