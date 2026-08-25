# Sweep — reader divergence on a short file declaring a foreign major

## 0. Disclosure

**Files read:** exactly one —
`/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (4495 lines).
No other file was read: no `docs/`, no ADRs, no `PLAN.md`, `OPEN-QUESTIONS.md`,
`AGENTS.md`, `README.md`, no `conformance/`, no `spec/registry.json`, no git
history, no web.

**Commands run:** `wc -l`, `grep -n` and `sed -n` over that one file; three
`python3` heredocs that read no file at all (a CRC-32C implementation plus
byte-buffer construction), and one `python3` heredoc that reads only
`tarn.md` and does whitespace-normalised regex search over it (because the
document is hard-wrapped and a line-oriented grep misses wrapped phrases).
Every quotation below was recovered by whitespace-normalised search, not by
line-oriented grep, except where a `sed -n` range is shown.

**Files written:** this file only. I did not read the directory it is in.

**Unrequested context.** Material appeared in my context before I began: a
project instruction file pointing at another in-repo file, an index of the
maintainer's private memory notes with titles, an environment block naming the
working directory, the git branch, working-tree status and several recent
commit subjects, plus a tool-server usage note. **None of it is part of the
specification and none of it is evidence about the specification.** I
disregarded all of it and do not repeat its contents. In particular I did not
follow the project instruction file's pointer, and I read none of the notes
or commits it named.

---

## 1. The paragraph under examination

`sed -n '3430,3447p'` — §21.2, lines 3430–3447 (hard wraps preserved):

```
3430  #### 21.2 File-scope violations
3431
3432  Outcome: reject-file. 36 conditions. A file declaring a format major
3433  other than 1 is neither conforming nor nonconforming under this text
3434  (§2.3, `[R-CNF-02]`), and the rows below whose subject is that
3435  file's *geometry* do not reach it: §6.2 puts the version gate ahead
3436  of every check but the trailer magic and the trailer CRC, so such a
3437  file is refused on capability grounds first. Four rows are outside
3438  that reasoning and do reach it, because their subject is a field
3439  fixed across every major (`[R-CNT-24]`): F8 and F1's trailer-magic
3440  instance, F14's trailer CRC — the two checks §6.2 places before the
3441  gate — and F6 with F1's front-block instance, which `[R-CNT-04]`
3442  places before other processing for a reader that already holds those
3443  bytes, one that would have to fetch them being free to defer or omit
3444  the check. F18 is not an exception but a case
3445  outside the premise: version_major = 0 declares no major at all and
3446  is permanently invalid in every one (§21.6).
3447
```

The paragraph is not inside a Markdown blockquote and is not labelled Note,
Example or Rationale, so it is normative text per §2.1 line 104–106:

> "All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative. `[R-CNF-01]`"

It carries no ALL-CAPS keyword, so it binds nothing under §2.1's BCP 14 clause
(lines 98–102), but it is a keyword-free declarative and is therefore not
inert.

The paragraph makes two load-bearing claims:

- (P1) an ordering claim: "§6.2 puts the version gate ahead of every check but
  the trailer magic and the trailer CRC";
- (P2) a closure claim: "**Four** rows are outside that reasoning and do reach
  it" — an exhaustive count.

---

## 2. §6.2's ordering language, quoted exactly

`sed -n '773,782p'` — §6.2, lines 773–782:

```
773  A reader MUST validate, in order: the trailer magic; the trailer CRC;
774  the version gate (§6.3) — only these touch fields whose positions are
775  fixed across all majors (`[R-CNT-24]`) — and then, those gates passed,
776  MUST validate all of the following before acting on the fields
777  involved: the flag gates (§6.3); committed_file_length equals the file
778  size (for a remote reader, the size reported by its transport) and is
779  a multiple of 64; dir_offset ≥ 16; dir_length ≥ 4; dir_offset +
780  dir_length ≤ F − 64; 1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0; reserved
781  bytes zero. Any failure is reject-file. The owning scope of the front
782  signature block and the trailer is the file. `[R-CNT-06]`
```

The ordered set is therefore **exactly eleven checks**:

- pre-gate (3): trailer magic; trailer CRC; version gate.
- post-gate (8): flag gates; `committed_file_length` = F; F multiple of 64;
  `dir_offset ≥ 16`; `dir_length ≥ 4`; `dir_offset + dir_length ≤ F − 64`;
  generation range; `file_id ≠ 0`; reserved bytes zero.
  (§24's `[R-VEC-02]`, line 4052, adds that these post-gate ones are
  "validated together": "§6.2's field gates are validated together, so a file
  failing two of them attributes to neither alone".)

§19.1 step 2 restates the same order (lines 2725–2729):

```
2725     2. **Trailer.** Fetch bytes [F − 64, F) and validate them in
2726        §6.2's fixed order — magic, trailer CRC, version gate, then the
2727        remaining field gates (`[R-CNT-06]`, `[R-CNT-07]`,
2728        `[R-CNT-08]`). The validated trailer is the session's snapshot
2729        (§9.5, `[R-LIF-05]`); no later step re-reads the file's end.
```

And §4.5 `[R-ENC-10]` (line 455–456) confers force on that order:

> "…and an explicit validation order (§6.2) governs where one is stated."

**The ordered set does not contain a minimum-file-size check.** See §4 below
for the search that establishes this.

### 2a. (P1) is already false on the paragraph's own next sentence

`[R-CNT-04]`, §6.1 lines 717–727, places a check ahead of everything in §6.2:

```
717  A reader whose open leaves bytes
718  [0, 16) **resident** — a local file read whole, a memory mapping, a
719  speculative suffix window that reached offset 0, or any transport
720  already holding them — MUST verify the full block by byte
721  equality before other processing, and MUST treat any mismatch as
722  reject-file.
```

So "the version gate ahead of every check but the trailer magic and the
trailer CRC" is untrue of the front-block check, which is ahead of the version
gate and of the trailer magic. The paragraph itself concedes this two
sentences later ("`[R-CNT-04]` places before other processing"), but does so by
*adding an exception* rather than by correcting (P1). (P1) is therefore not a
statement §6.2 supports; it is an over-claim the paragraph then patches
case-by-case. That matters because (P1) is the sole stated ground for
excluding every non-excepted row.

---

## 3. `[R-RDR-02]`, quoted exactly — what it fixes about *when*

`sed -n '2763,2794p'` — §19.2, lines 2763–2794:

```
2763  #### 19.2 Validation timing
2764
2765  A reader MUST detect each violation whose detection this
2766  specification obliges readers to make — a violation whose assigned
2767  detector is the verifier (§2.4, `[R-CNF-12]`) imposes no reader
2768  obligation — no later than the reader's first reliance on the
2769  structure that carries it:
2770
2771  - **at open:** the front signature block, for a reader whose open
2772    leaves it resident (`[R-CNT-04]`), the trailer, the directory
2773    region and its record walk, and the layer-name namespace
2774    (§19.1's steps);
...
2786  Failure at any point takes the violated rule's own outcome and
2787  scope — in particular, index-chain failures take layer scope
2788  (`[R-IDX-04]`) although their detection point is tile use. A
2789  reader MAY detect any violation earlier (`[R-CNF-12]`); it MUST
2790  NOT return data whose governing structure has not passed the
2791  validation this rule requires at its tier. Structures a request
2792  never relies on impose no detection obligation beyond the open
2793  steps: a violating record in a layer never accessed leaves every
2794  other layer's reads conforming. `[R-RDR-02]`
```

**What `[R-RDR-02]` fixes is the *latest* permissible detection point, and
nothing else.** Its own (non-normative) Rationale, lines 2796–2801, says so:

> "The rule fixes the *latest* detection point, so the served-versus-failed
> boundary is deterministic: no conforming reader returns data its tier's
> validation would have refused. Earlier detection stays licensed, so a
> stricter reader can reject a nonconforming file sooner — divergence is only
> ever toward earlier rejection, never toward silent acceptance."

So the normative clause **"A reader MAY detect any violation earlier"** is
unqualified. `[R-RDR-02]` supplies no *earliest* bound; the only earliest
bounds in the document are the two explicit orders — §6.2's eleven-item order
and `[R-CNT-04]`'s "before other processing".

`[R-CNF-04]`, §2.3 lines 172–177, binds the reader to every register row whose
detector is the reader:

> "A reader MUST detect every violation the error register (§21) assigns to the
> reader as its detector, and apply the outcome class this specification
> assigns to each"

and §19.1's preamble, lines 2702–2708, makes the register the authority on
what is due at each tier:

```
2702  Each step names the checks its tier's structures turn on. Those
2703  enumerations are not the complete inventory of what a reader
2704  detects at that tier: §21's register is, and `[R-CNF-04]` binds a
2705  reader to every register row whose detector is the reader, at the
2706  tier that row's *Detected* cell names (§21.1). A row this section
2707  does not restate is due at its own tier all the same, with its
2708  governing rule's own outcome.
```

---

## 4. The minimum-size rule and its (absent) position in §6.2's order

`[R-CNT-27]`, §5.1, lines 575–579, quoted exactly:

```
575  No conforming file is shorter than 128 bytes: the front signature
576  block, a directory of at least 4 bytes at an offset of at least 16,
577  and the 64-byte trailer at a 64-aligned offset cannot be satisfied in
578  fewer. A reader MUST treat a shorter file as a validity error at file
579  scope. `[R-CNT-27]`
```

Its register row, §21.2 line 3454, quoted exactly:

```
| F5 | File size is below the 128-byte minimum, so the front block, directory, pre-trailer pad and trailer cannot all fit | F (physical file size); committed_file_length | reader | open | `[R-CNT-27]` (R-CNT-01, R-CNT-06) |
```

Detector **reader**; Detected **open**; two instances, the **first of which is
`F` itself** — the physical file size, not a trailer field.

`[R-ERR-05]`, §21.9 lines 3821–3823, restates it as a hard limit:

> "…and no conforming file shorter than 128 bytes (§5.1, `[R-CNT-27]`)."

`[R-CNF-08]`, §2.4 lines 245–247, converts "validity error at file scope" into
an outcome:

> "The phrase 'a validity error at the owning scope' means the reader outcome
> for that scope: file → reject-file, layer → reject-layer, tile →
> reject-tile."

### Search establishing that §6.2's order has no minimum-size item

Whitespace-normalised regex over the whole file (the document is hard-wrapped;
line-oriented grep would miss wrapped phrases). Every hit for each pattern was
printed and inspected.

| Pattern searched (normalised) | Hits | Lines |
|---|---|---|
| `shorter than 128` | 2 | 575 (§5.1, `[R-CNT-27]`), 3823 (§21.9, `[R-ERR-05]`) |
| `128` (line-oriented, cannot wrap) | 12 | 575, 581, 584, 1669, 3454, 3823, 4111, 4139, 4142, 4149, 4151, 4167 |
| `R-CNT-27` | 3 | 579, 3454, 3823 |
| `in order` | 9 | 294, 298, 773, 1008, 1172, 1604, 2712, 2965 — only **773** is §6.2's |
| `version gate` | 3 | 774, 2726, 3435 |
| `minimum` | 15 | none inside §6 |

**Result: `[R-CNT-27]` is cited at exactly three places — §5.1 where it is
stated, F5's row, and §21.9's finding-aid list. It is cited nowhere in §6, and
appears nowhere in §6.2's eleven-item ordered list or in §19.1's steps.**
The line-oriented `128` scan (a token that cannot wrap, so the scan is sound)
returns no hit anywhere in lines 695–869, i.e. nowhere in all of §6.

**Derivation D1.** §6.2's order is an order over the eleven checks it
enumerates. `[R-CNT-27]`'s check is not one of them. §6.2 therefore does not
order `[R-CNT-27]`'s check relative to the version gate — in either direction.
`[R-RDR-02]` gives `[R-CNT-27]`'s check a *deadline* (open, per F5's Detected
cell) and expressly licenses detection earlier. Nothing in the document gives
it a floor. **So a reader that tests F < 128 before fetching the trailer is
doing something the document licenses and forbids nowhere.**

Consequently (P1) — the paragraph's stated ground for excluding the
non-excepted rows — is simply inapplicable to F5: there is no §6.2 ordering
that puts the version gate ahead of F5's check, because §6.2 does not contain
F5's check at all.

### Does the exclusion criterion even name F5?

The criterion is "the rows below whose subject is that file's *geometry*"
(line 3434–3435). Every occurrence of the stem `geometr` in the document:

```
91, 1045, 1445, 1472, 1931, 2823, 3007, 3043, 3049, 3050, 3435, 3514, 3525,
3847, 3983, 4255
```

Inspected: **every one except 3435 uses "geometry" for a layer's array
geometry** — rank, extents, tile extents, linearization. E.g. §11.1's heading
"Geometry and its validity floor" (line 1470) and §11.1 line 1472: "The owning
scope (§2.4) of a layer's geometry and linearization fields…"; L32's row (line
3525): "A layer geometry field whose floor is 1 is 0 | rank d; channel count C;
tile extent Tᵢ". No §21.2 row has array geometry as its subject — §21.2's rows
are container rows. So on the document's own usage, line 3435's "geometry" has
no established referent among §21.2's rows.

**Derivation D2.** The paragraph's exclusion has two parts that do not agree
about F5. Its *criterion* — "rows whose subject is that file's geometry" — does
not, on this document's uniform usage of "geometry", pick out F5, whose subject
is the physical file size F. Its *closure claim* — "**Four** rows are outside
that reasoning" — implies by exhaustion that F5 is excluded. The paragraph is
therefore internally undecided about F5.

### And no precedence rule resolves it

§21.1 line 3370–3371 gives a precedence rule, but only for **rows**:

> "…but each row *restates* its governing rule, and where a row and the rule it
> cites diverge, **the rule governs**."

and line 3383–3385 extends it only to §21.6's **entries**:

> "§21.6's entries restate their governing rules on the same terms a row does,
> and where such an entry and the rule it cites diverge, the rule governs there
> too."

§21.2's *introductory paragraph* is neither a row nor a §21.6 entry.
**I searched for any clause giving precedence to §21's prose over a numbered
requirement, or vice versa** — patterns `the rule governs`, `governs`,
`diverge`, `restates` — and found only the two clauses above. **There is no
stated precedence between §21.2's paragraph and `[R-CNT-27]`'s ALL-CAPS MUST.**
This is a well-searched absence, not an undiscovered rule.

---

## 5. The three files

CRC-32C per `[R-ENC-09]`, §4.5 lines 441–444: Castagnoli 0x1EDC6F41, reflected
in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian. My
implementation was validated against the document's own check vector (§4.5
lines 446–450): `crc32c("123456789") = 0xE3069283` ✓ and `crc32c(b"") =
0x00000000` ✓ — printed output: `check vector OK: 0xE3069283`.

Field positions across majors come from `[R-CNT-24]`, §6.3 lines 800–807:

```
800  In every format major version, permanently: the final 64 bytes of a
801  file contain the trailer magic at F − 64, version_major and
802  version_minor at F − 56, and a CRC-32C at F − 4 covering bytes
803  [F − 64, F − 4); and the front signature block (§6.1) is constant. A
804  future major MAY redefine only the remaining 48 trailer bytes and MUST
805  NOT grow the trailer; additional space comes from structures placed
806  before it. The format-major-1 trailer has zero slack: every byte is
807  assigned. `[R-CNT-24]`
```

Note what `[R-CNT-24]` fixes across majors: magic position, version-field
position, terminal CRC position and coverage, and the front block. It does
**not** fix 64-alignment of F across majors, and it does not fix
`committed_file_length`'s position (trailer offset 40) across majors.

Front block constant, §6.1 line 703–704: `89 54 41 52 4E 0D 0A 1A` then 8 zero
bytes. Trailer magic, §6.2 line 746: `8A 4E 52 41 54 0D 0A 1A`.

### File A — F = 32, "declaring major 2"

```
[0,16)  89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00   (front block, correct)
[16,32) 00 × 16
```

Computed positions: `F − 64 = -32`, `F − 56 = -24`.

**Derivation D3 — the file cannot declare a major.** `[R-CNT-24]` locates
version_major at `F − 56`. At F = 32 that offset is negative and there are no
"final 64 bytes of a file" (line 800). No byte of this file is version_major
under any major. **The premise of §21.2's paragraph — "a file declaring a
format major other than 1" — is unsatisfiable at F = 32.** The task's File A
is, like F18, "a case outside the premise". A 32-byte file *declaring* major 2
cannot be built.

What the two readers report:

- Reader-§6.2 cannot execute §19.1 step 2: "Fetch bytes [F − 64, F)" is
  `[-32, 32)`. The document specifies no behaviour for that fetch. What it does
  specify is `[R-LIF-05]`, §9.5 lines 1271–1274: *"The default read path is
  trailer-at-end-or-fail: a reader that finds no valid trailer in the final 64
  bytes MUST report the file torn or invalid and MUST NOT scan backward."*
  → **reject-file, reported as torn/invalid.**
- Reader-F5-first: F = 32 < 128 → `[R-CNT-27]` "A reader MUST treat a shorter
  file as a validity error at file scope" → **reject-file, a validity error.**
- Either reader with bytes [0,16) resident (a 32-byte local file read whole
  necessarily leaves them resident) additionally owes `[R-CNT-04]`'s equality
  check "before other processing"; here it passes.

**Verdict A: the two readers agree.** Both reject-file, both report a defect in
the bytes rather than a capability refusal, and both verifiers report
*nonconforming* (§2.3 line 209–211: "An established violation takes priority").
There is no divergence at 32 bytes, and the reason is that the paragraph's
premise cannot be met there. **This is a real negative result.**

### File B — F = 100, declaring major 2

```
[0,16)    89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00   front block, correct
[16,36)   00 × 20
[36,44)   8a 4e 52 41 54 0d 0a 1a      trailer magic at F−64  ✓
[44,46)   02 00                        version_major = 2 (u16 LE, §4.1 [R-ENC-01])
[46,48)   00 00                        version_minor = 0
[48,96)   00 × 48                      the 48 bytes a future major MAY redefine
[96,100)  f1 b3 16 3b                  CRC-32C = 0x3B16B3F1 over [36,96) = [F−64, F−4) ✓
```

Recomputation printed: `crc32c(B[36:96]) = 0x3B16B3F1`, stored
`0x3B16B3F1` — match. `100 mod 64 = 36`.

This file satisfies every position `[R-CNT-24]` fixes across majors: magic at
F−64 is exact, version fields at F−56 are present, the terminal CRC at F−4
verifies over [F−64, F−4). It declares major 2. And F = 100 < 128.

**Reader A — follows §6.2's order.**

1. Bytes [0,16) resident (local, 100-byte file read whole) → `[R-CNT-04]`
   equality check: passes.
2. §19.1 step 2, §6.2 order: trailer magic at [36,44) → passes.
3. Trailer CRC → passes.
4. Version gate, `[R-CNT-07]` §6.3 lines 791–796:
   *"A reader MUST reject-file when version_major is 0 (invalid) or is a major
   it does not implement, and the diagnostic for an unimplemented major SHOULD
   be distinct from both 'not a TARN file' and 'corrupt' (e.g. 'TARN format
   major N; this reader supports major 1') — a reader that reports an
   unimplemented major as corruption misleads users into discarding files that
   current software reads."*
   → **reject-file on capability grounds**, diagnostic "TARN format major 2;
   this reader supports major 1", which §6.3 SHOULDs be distinct from
   "corrupt".
5. §6.2's post-gate list is never reached ("those gates passed" is false).
   `[R-CNF-02]` §2.3 lines 142–145: *"a file declaring another major is neither
   conforming nor nonconforming under it: a reader refuses such a file on
   capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding
   about its bytes."*
   As a verifier: §2.3 lines 193–197 give **cannot establish** — *"the last
   where some requirement is one it is unable to check on a capability or
   resource ground, as when the file names a format major version it does not
   implement"*.

**Reader B — takes F5 at open, which `[R-RDR-02]` licenses.**

1. §19.1 step 1: *"**End of file.** Obtain the transport-authoritative file
   size F (`[R-CNT-10]`)."* F = 100.
2. F5's Detected cell is *open*; `[R-CNF-04]` obliges the check; `[R-RDR-02]`
   sets open as the **latest** point and says *"A reader MAY detect any
   violation earlier"*. Nothing orders F5's check after the version gate,
   because §6.2's order does not contain it (Derivation D1).
3. `[R-CNT-27]`: F = 100 < 128 → *"A reader MUST treat a shorter file as a
   validity error at file scope"* → **reject-file as a validity error**,
   diagnostic "corrupt / not a valid TARN file".
   As a verifier: a violation is *established*, so §2.3 lines 209–211 force
   **nonconforming** — *"An established violation takes priority: a verifier
   that has established any violation reports *nonconforming*, however many
   requirements it was unable to check, and *cannot establish* is available
   only to a traversal that established no violation."*

**Verdict B: the two readers diverge, and both have a conforming defence.**

| | Reader A | Reader B |
|---|---|---|
| Outcome class | reject-file | reject-file |
| Ground | capability (foreign major) | validity error (file too short) |
| Diagnostic §6.3 requires be distinguishable | "format major 2 unsupported" | "corrupt" |
| Verifier verdict (§2.3) | **cannot establish** | **nonconforming** |
| Defence | §21.2 ¶ (P1)+(P2); §6.2 line 773 "MUST validate, in order"; `[R-ENC-10]` "an explicit validation order (§6.2) governs" | `[R-CNT-27]` unqualified MUST; F5 Detector *reader* / Detected *open*; `[R-CNF-04]`; `[R-RDR-02]` "MAY detect any violation earlier"; D1 (no §6.2 ordering exists to violate) |

The two verifier verdicts are not merely differently-worded: they are two of
the three verdicts `[R-CNF-11]` defines, and *nonconforming* directly
contradicts `[R-CNF-02]`'s "neither conforming nor nonconforming under it".
The document also treats the reader-facing distinction as normatively real:
§6.3 SHOULDs the foreign-major diagnostic be distinct from "corrupt", and
`[R-ERR-04]` §21.9 lines 3786–3790 makes the parallel distinction a MUST for
resource refusals — *"a refusal on resource grounds MUST be reported as a
resource limit and not as a validity error: the two send a user to opposite
remedies, and a reader that reports 'too large' as 'corrupt' invites the
deletion of intact data."*

Secondary, weaker divergence axis on the same file: §6.2's opening declarative,
line 741–742 — *"The trailer occupies the final 64 bytes of the file, beginning
at a 64-aligned offset (equivalently: F mod 64 = 0)."* — is keyword-free
normative text, and 100 mod 64 = 36. A third reader could refuse on that
ground. But `[R-CNT-24]` deliberately does not carry 64-alignment across
majors, and §6.2's own list places "is a multiple of 64" *after* the version
gate, so a §6.2-following reader cannot reach it. I record this as an
additional unresolved axis, not as the primary finding.

### File C — F = 200, declaring major 2

```
[0,16)     front block, correct
[16,136)   00 × 120
[136,144)  8a 4e 52 41 54 0d 0a 1a      magic at F−64 ✓
[144,146)  02 00                        version_major = 2
[146,148)  00 00                        version_minor = 0
[148,196)  00 × 48
[196,200)  f1 b3 16 3b                  CRC-32C = 0x3B16B3F1 over [136,196) ✓
```

Recomputation printed: `0x3B16B3F1` = stored. `200 mod 64 = 8`. F = 200 ≥ 128,
so **F5 does not fire**.

- Reader A: magic ✓ → CRC ✓ → version gate → reject-file, capability ground,
  "major 2 unsupported"; verifier: *cannot establish*.
- Reader B (the F5-first reader): F5's predicate is false; it has nothing to
  fire on earlier. What else could it try? The candidates are F13
  (`committed_file_length` not a multiple of 64) and F17
  (`committed_file_length` ≠ transport size). Both read trailer offset 40,
  a position `[R-CNT-24]` does **not** fix across majors, so under major 2
  those bytes are not `committed_file_length`; and both checks *are* in §6.2's
  post-gate list, genuinely after the version gate, so §21.2's (P1) holds of
  them. Reader B therefore reaches the version gate too.

**Verdict C: the two readers agree** — reject-file on capability grounds,
foreign major, verifier *cannot establish*. File C is the control that shows
the divergence is not about foreign majors generally: it is specifically about
the band **64 ≤ F < 128**, where F5's predicate is true *and* the version field
exists.

---

## 6. The band, stated precisely

Let F be the physical file size of a file whose bytes at F−64 are the trailer
magic and whose CRC at F−4 verifies.

- **F < 64:** version_major has no location (`F − 56 < 0`). No major is
  declared. The paragraph's premise fails; readers agree (File A).
- **64 ≤ F < 128:** version_major exists at F − 56 and F5's predicate is true.
  Two checks are simultaneously due at *open*, with no ordering between them.
  **Readers diverge** (File B).
- **F ≥ 128:** F5's predicate is false. Readers agree (File C).

The divergent band is exactly **64 ≤ F < 128**, i.e. F ∈ {64, 65, …, 127}, 64
sizes in all. At F = 64 the trailer at [F−64, F) = [0, 64) overlaps the front
signature block, so `[R-CNT-04]`'s equality check and the trailer magic
contradict each other and either reader rejects — a further degenerate case the
document does not address. **The clean divergent range is 65 ≤ F ≤ 127: 63
file sizes.**

---

## 7. What the document states, implies, and does not decide

**States (verbatim, cited above):**
- §6.2 line 773: the eleven-check order, and only those eleven.
- §19.2 line 2789: "A reader MAY detect any violation earlier".
- §5.1 line 578: "A reader MUST treat a shorter file as a validity error at
  file scope" — no major-version qualification.
- §21.2 line 3454: F5, detector *reader*, detected *open*, first instance "F
  (physical file size)".
- §21.2 line 3437: "**Four** rows are outside that reasoning and do reach it".
- §2.3 lines 142–145 and 209–211: capability refusal is "not a finding about
  its bytes"; an established violation forces *nonconforming*.

**Implies by derivation written out above:**
- D1: §6.2 imposes no ordering on `[R-CNT-27]`'s check, because the check is
  not in §6.2's list; so (P1) cannot support F5's exclusion.
- D2: the paragraph's criterion ("geometry") and its count ("four") disagree
  about F5, on the document's own uniform usage of "geometry".
- D3: at F < 64 no major is declared, so the paragraph's premise is
  unsatisfiable there.
- Both Reader A and Reader B have a conforming defence for File B, and they
  produce different verifier verdicts.

**Does not decide (well-searched absences):**
- Whether `[R-CNT-27]` reaches a file declaring a foreign major. Searched:
  `R-CNT-27` (3 hits, all listed), `shorter than 128` (2 hits), `128`
  line-oriented (12 hits), `minimum` (15 hits) — none qualifies `[R-CNT-27]`
  by major, and none places it in an order.
- Any precedence between §21.2's introductory paragraph and a numbered
  requirement. Searched `the rule governs`, `diverge`, `restates` — the only
  precedence clauses are §21.1's, and they cover *rows* and §21.6 *entries*
  only.
- What a reader does when F < 64 and the trailer fetch `[F − 64, F)` is
  ill-formed. Only `[R-LIF-05]`'s "no valid trailer in the final 64 bytes"
  covers it, and only by reading "finds no valid trailer" charitably.
- Whether F must be 64-aligned under a foreign major. `[R-CNT-24]` does not say;
  §6.2's alignment declarative sits in the major-1 trailer section.

**Supplied by me (not findings):** the choice of 100 and 200 bytes; the
all-zero filler; the observation that the divergent band has 63 clean members.

---

## 8. Appendix — exact tool output

```
$ wc -l spec/tarn.md
    4495 spec/tarn.md

$ python3 (CRC + file construction; reads no file)
check vector OK: 0xE3069283

FILE A  F=32 : len 32
  front [0,16) = 89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00
  F-64 = -32   F-56 = -24   F-4 = 28

FILE B  F=100: len 100  F-64 = 36  F-56 = 44  F-4 = 96
  magic  [36,44) = 8a 4e 52 41 54 0d 0a 1a
  vermaj [44,46) = 02 00 = u16 LE 2
  vermin [46,48) = 00 00
  crc    [96,100)= f1 b3 16 3b = 0x3B16B3F1 over bytes [36,96)
  recompute crc32c(B[36:96]) = 0x3B16B3F1  stored 0x3B16B3F1
  100 mod 64 = 36

FILE C  F=200: len 200  F-64 = 136  F-56 = 144  F-4 = 196
  magic  [136,144) = 8a 4e 52 41 54 0d 0a 1a
  vermaj [144,146) = 02 00 = 2
  crc    [196,200) = f1 b3 16 3b = 0x3B16B3F1 over [136,196)
  recompute =0x3B16B3F1
  200 mod 64 = 8
```

Whitespace-normalised search hits (pattern → line numbers), all inspected:

```
"version gate"                    -> 774, 2726, 3435
"in order"                        -> 294, 298, 773, 1008, 1172, 1604, 2712, 2965
"shorter than 128"                -> 575, 3823
"first reliance"                  -> 2768
"MAY detect any violation earlier"-> 2789
"before other processing"         -> 721, 2721, 3442
"capability grounds"              -> 144, 3437
"ahead of"                        -> 3435
"foreign format major"            -> 3784
"cannot establish"                -> 194, 211, 221, 2419, 2422, 2527, 2533, 4492
"final 64 bytes"                  -> 334, 564, 741, 800, 833, 1251, 1273, 1301, 4144
"F − 64"                          -> 752, 780, 801, 803, 934, 1345, 1347, 1349,
                                     2069, 2725, 3559, 4304, 4307
"geometr" (line-oriented)         -> 91, 1045, 1445, 1472, 1931, 2823, 3007, 3043,
                                     3049, 3050, 3435, 3514, 3525, 3847, 3983, 4255
"R-CNT-27" (line-oriented)        -> 579, 3454, 3823
"128" (line-oriented)             -> 575, 581, 584, 1669, 3454, 3823, 4111, 4139,
                                     4142, 4149, 4151, 4167
```
