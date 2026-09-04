# 0121. No writer under this text originates an ignore-lane flag bit

- Status: Accepted (resolves Q-B9)
- Date: 2026-09-03
- Covers: §6.3 `[R-CNT-08]`; §20.3 step 6; §20.5 `[R-WRT-06]`; Appendix G item 8
- Confirm: none

## Context

§6.3's `[R-CNT-08]` bound *"a writer creating a file under this text"* to
flags = 0, carved a compactor out of that phrase expressly because *"its
output is a new file"*, and gave an updater one obligation: copy unknown
ignore-lane bits forward and never clear them. Nothing said an appender may
not *set* an ignore-lane bit its input never carried. Round 27's writer walk
found it, graded it byte-level, and the hand-check confirmed the fork; the
ledger carried it as Q-B9, gating G3.

**The fork on the page.** Take Appendix A's 128-byte file as generation 1.
Two appenders commit generation 2 from it with the same instruction — a
complete directory at 128, a pad to 192, a trailer at 192 with F = 256 and the
same file_id. Appender A copies the input's ignore-lane bits forward; there
are none, so flags = 0 and the trailer's CRC is 0xE3AE15E8. Appender B writes
flags = 0x00010000, bit 16, and the CRC is 0xA3BE7406; the two trailers differ
at one byte of the flags field and the four CRC bytes. B's file is conforming
in terms — §21.6: *"An ignore-lane flag bit (16–31) is set | Ignored; the file
is conforming"* — and under the letter B is a conforming appender: it created
no file, copied what there was, cleared nothing. Under the other reading of
*creating a file* B violated `[R-CNT-08]`. A conforming file that one reading
lets a conforming actor emit and the other does not is the byte-level test's
second limb, and only an appender can produce this file: a creator writes 0
and a compactor writes exactly the input's bits at a fresh file_id.

**What the bit then does.** Every later compactor carries bit 16 for the life
of the file, every updater must never clear it, every reader under this text
ignores it, and a reader under a future minor that defines bit 16 finds a
claim about the file that nobody who knew the bit's meaning made, beside
version_minor = 0 — which `[R-CNT-26]`'s SHOULD-level floor cannot flag.

**The priced sweep of 2026-08-26** found that binding every writer to
flags = 0 deadlocks with copy-forward on any nonzero-lane input, that
licensing appenders to originate widens the fork, and that making step 6's
enumeration exhaustive works but reuses the actor-relative word *unknown* in a
way that would oblige a bit's recogniser to clear it. It also named a fourth
option, a register row for a bit set beside version_minor = 0.

**The maintainer asked what the flags are for, if a writer must always write
0**, and what distinguishes them from the trailer's reserved bytes. The
answers are the ground of this decision and are recorded here. The flags are
a reservation for later versions of this text, not a field this version's
writers populate: §6.3 says ignore-lane bits *"are defined by later minor
versions"*, §4.3 lists new ignore-lane bits among the four vehicles of format
growth, and `[R-EXT-02]` withholds an experimental range from the lanes, so
neither this text's writers nor applications have a bit to set. A writer
under a later minor sets the bit it defines and writes that minor; this
text's tools carry the bit through, as MU and PE travel with records their
tools never heard of. Copy-forward stops an old tool stripping a feature flag;
the bar stops an old tool asserting one. The trailer's three reservations
differ in what an old reader does on meeting a use: reserved bytes are
corruption (F15) and only a new major can use them; an incompat bit is a
clean refusal (F19), ADR-0025's *"refuse lever that spares the major"*; an
ignore-lane bit is ignored and the file served. What they share is that none
is set by a writer under this text — which the ignore lane's wording alone
had left unsaid.

## Decision

**No writer under this text originates an ignore-lane bit.** `[R-CNT-08]` now
says so in terms and gives the reason — *"this text defining none for it to
mean anything by, so a bit is set only by a writer under the later minor
version that defines it and carried by every tool after"* — and binds the
updater in BCP 14: it *"MUST copy forward unknown ignore-lane bits of the
file it modifies, MUST NOT clear them, and MUST NOT set any other"*. The
compactor sentence in §6.3 and `[R-WRT-06]`'s in §20.5 gain *"and sets no
other"* / *"and set no other"*; §20.3 step 6's trailer enumeration reads
*"unknown ignore-lane flag bits copied forward and no other set"*; Appendix
G item 8's compactor clause matches. A creator's flags = 0 is unchanged.

Stated as a bar on origination rather than on the field's value, the
obligation cannot deadlock with copy-forward: an appender extending a file
whose live trailer carries bit 16 writes bit 16 and nothing else.

## Consequences

**Q-B9 is resolved**, for every writer tier, without a ruling on §20.1's
tier word *creator*. Appender B above is a nonconforming writer; its file
stays conforming, as `[R-CNF-02]` provides for every obligation this text
places on a writer's conduct — the predicate binds the bytes, the rule binds
the actor. **Nothing moves in the register or the corpus**, and no reader
behaviour changes.

**The witness option is not taken.** Registering *an ignore-lane bit set with
version_minor = 0* as a violation would make B's file itself nonconforming
and verifiable, at the cost of a §21.2 row, its vectors, and a MUST on later
minors' writers to raise version_minor whenever they set a bit — a rule
about texts that do not yet exist, made here. It remains available as a
future ledger entry if a verifiable form is ever wanted; nothing in this
decision forecloses it.

## Alternatives rejected

- **Creators only, appenders licensed to originate.** Widens the fork rather
  than closing it, leaves *creator* ambiguous against §20.1, and runs against
  `[R-EXT-02]`'s ground for withholding an experimental range from the lanes.
- **Every writer bound to flags = 0.** Adoptable only in the form taken here;
  as a value rule it is unsatisfiable beside copy-forward.
- **Step 6's enumeration made exhaustive, §6.3 untouched.** Closes the fork
  for appenders and leaves a compactor's route stated in two places; taken in
  substance for step 6, with the rule stated once where it lives.

## Precedent

- **ADR-0025**, which reserved the lanes and wrote *"updaters MUST copy
  unknown ignore-lane bits forward (else the first older-tool append strips
  them)"* — this decision is the other half of that sentence.
- **ADR-0091**, that a rule's reach is settled by an ADR and not in a repair
  slot; round 27 sent this to the ledger on that ground.
- **ADR-0117** decision 4, and `[R-CNF-02]`: a writer obligation declared
  where it arises, binding the actor and not the bytes.
