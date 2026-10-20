# Word-diff preflight over `58d3201`..`0c3ab26`, spec/tarn.md

For every commit in the range touching `spec/tarn.md`: the diff's removed and added lines as two texts, blockquote prefixes dropped, words tokenised as `pass/propose.py` does (`[\w'’]+`), and the Counter difference printed as words lost and words gained. Expected: connectives, inflections, capitals, the recorded swaps and the dropped pointers; anything else is a transcription defect.

## `58d3201` Readable: §9.1–§9.2 — maintainer's edits, reviewed

- removed lines 20, added lines 21; words 220 → 220
- **lost:** Bytes, There, a, and, being, every, rewrite, whose, writing
- **gained:** All, Because, Every, The, block's, bytes, is, there, with

## `1df7b0d` Readable: §9.2 — the strict-increase Note's premise stated as step 3's requirement, not the first Note's

- removed lines 11, added lines 11; words 127 → 127
- **lost:** an, by, directory, earlier, forbids, generation's, reusing, so, such, there
- **gained:** it ×2, 3, appends, as, own, performs, reads, step, that

## `48e65f4` Readable: §9.2 — maintainer's edit, reviewed: the crash Example's lead-in in sentences

- removed lines 3, added lines 4; words 31 → 38
- **lost:** in ×2
- **gained:** In ×3, is ×2, it ×2, following, the

## `44f113d` Readable: §9.2–§9.3 — maintainer's edits, reviewed; §9.3's first Note cites the rules its derivation rests on

- removed lines 17, added lines 19; words 192 → 225
- **lost:** checkable, makes, never, no, one, what
- **gained:** R ×4, LIF ×3, 02 ×2, and ×2, steps ×2, 's, 01, 06, 1, 3, 5, CNT, No, a, as, beside, by, conforming, derives, forced, generation, it, not, performs, promised, rather, than, the, them, writer, yield

## `8b1eefe` Readable: §9.4–§9.5 — maintainer's edits, reviewed; §9.5's Note says which bytes it means

- removed lines 9, added lines 10; words 103 → 120
- **lost:** residue ×2, One, Residue, a, commit, completes, past, this, violates
- **gained:** bytes ×3, file ×2, in ×2, TARN, The, This, are, beyond, but, case, committed, extra, is, length, one, only, present, such, supports, the, those, violate, which

## `64b6e5e` Readable: §7.2, §7.4 — residue stated as the register states it; R-CNT-12 listed

- removed lines 32, added lines 34; words 382 → 403
- **lost:** residue ×4
- **gained:** bytes ×4, remaining ×4, after ×3, complete ×3, last ×3, record ×3, the ×3, sub ×2

## `a4ac2d2` Readable: §2.3, §9.6, §20.1, Appendix H — ADR-0134 ported: truncation to the last committed state is an updater's operation; R-LIF-09 added

- removed lines 58, added lines 78; words 687 → 949
- **lost:** (none)
- **gained:** it ×13, the ×13, is ×12, state ×10, committed ×9, file ×9, to ×9, R ×8, and ×8, that ×8, LIF ×7, a ×6, its ×6, A ×5, leaves ×5, length ×5, 09 ×4, an ×4, as ×4, last ×4, tool ×4, truncates ×4, updater ×4, 9 ×3, byte ×3, no ×3, not ×3, so ×3, 06 ×2, 6 ×2, MUST ×2, above ×2, below ×2, binds ×2, bytes ×2, commit ×2, earlier ×2, equal ×2, every ×2, operation ×2, physical ×2, re ×2, truncation ×2, 's, 01, 05, 1, 20, 7, CNF, It, Its, NOT, bound, candidate's, carries, cautions, certifying, default, describe, does, established, exactly, forward, free, in, latent, leave, modifies, modify, of, office, one, output, path, probe, produces, provides, reach, read, removes, reports, requires, rollback, section's, state's, there, this, too, travels, truncate, truncating, verification, verifier's, verifies, violation, well, what, with

## `2d3e790` Readable: §9.6 — ADR-0134's erratum ported: "the candidate's committed file length" for "that committed file length"

- removed lines 8, added lines 9; words 101 → 102
- **lost:** that
- **gained:** candidate's, the

## `66b0f01` Readable: §9.7 — the claimants paragraph: a claimant glossed from R-CNT-02 and §5.2; a record claims nothing in its own right

- removed lines 14, added lines 15; words 157 → 183
- **lost:** a ×2, claimant ×2, second ×2, beside, covering, enters, is, names, not, on, reaching, those, traversal, walk, which
- **gained:** the ×4, claimed ×2, that ×2, 2, 5, Its, They, adds, again, and, are, as, being, belong, bytes, claiming, committed, covers, directory, does, each, extent, in, into, it, its, live, no, own, partitions, range, reached, region, rest, right, slack, state, structures, to

## `f96eb0b` Readable: §10 — maintainer's edit, reviewed: the identifier spaces' lead-in a sentence

- removed lines 1, added lines 1; words 12 → 13
- **lost:** and
- **gained:** are, but

## `dc66fc9` Readable: §11.1 — the growth Rationale in plain language; the §20.3 summary kept, the two stated-once sentences kept

- removed lines 22, added lines 22; words 253 → 265
- **lost:** may ×6, a ×2, and ×2, at ×2, be ×2, does ×2, its ×2, commit, content, creation, do, either, emitted, governs, holding, included, layer's, normatively, only, or, other, produces, qualify, raises, remaining, states, supersedes, that, tiles, way, what
- **gained:** is ×4, the ×4, it ×3, stays ×3, when ×2, 4's, Growth, In, That, What, allowed, as, both, can, change, cheap, created, emits, every, file, holds, includes, index, last, layer, leaves, never, of, on, resulting, rises, same, say, short, since, step, superseded, their, though, tile, to, was, where

## `0b9ed09` Readable: §11.2 — the ceiling-division Note and the Example without dashes

- removed lines 8, added lines 7; words 74 → 75
- **lost:** whose
- **gained:** and, its

## `0db63fe` Readable: §11.4 — the linearization Note in ordinary sentences

- removed lines 6, added lines 7; words 57 → 68
- **lost:** Column, about, carried, ecosystems, fixes, from, it, mapping, nothing, same, says, their, write
- **gained:** its ×2, A, It, and, as, carries, column, decides, ecosystem, gets, how, is, maps, no, notion, of, only, or, such, that, travels, which, writes

## `c21a48d` Readable: §11.4 — the ordinals Example in sentences, its three arrows gone

- removed lines 7, added lines 8; words 85 → 103
- **lost:** Spatial, The, carrying, ordinals
- **gained:** ordinal ×4, has ×3, is ×2, spatial ×2, whose ×2, 1, Take, Under, and, carries, linearization, that, the, with

## `3ed24c3` Readable: §12.2 — maintainer's edit, reviewed: the type field's values fall into five ranges

- removed lines 10, added lines 11; words 116 → 121
- **lost:** (none)
- **gained:** fall, five, into, ranges, type

## `fd87472` Readable: §12.3, §13.1 — maintainer's edits, reviewed; R-TYP-10 listed

- removed lines 3, added lines 3; words 32 → 35
- **lost:** (none)
- **gained:** of, that, with

## `58dd3bb` Readable: §13.2 — the fill Rationale points at the reader's exemption from screening value bytes

- removed lines 1, added lines 2; words 9 → 22
- **lost:** (none)
- **gained:** 08, 14, 2, R, Readers, SER, bytes, for, it, need, not, screen, value

## `b96560c` Readable: §14.1 — the value sequence's two bullets in short sentences; R-SER-01's line extended

- removed lines 9, added lines 10; words 102 → 124
- **lost:** of ×3, the ×2, C, adjacent, all, exactly, values, with
- **gained:** in ×4, through ×3, Its ×2, The ×2, order ×2, positions ×2, runs ×2, tile ×2, and, each, else, every, is, it, nothing, one, position, sit, so, that, together, within

## `ff7bac9` Readable: §14.1 — maintainer's edit, reviewed: the layout field's value set reordered; R-SER-06 listed

- removed lines 5, added lines 5; words 60 → 62
- **lost:** Field, values
- **gained:** and, field, for, the

## `52dbc95` Readable: §14.2 — the boolean-byte Rationale argues the rule, not the draft it replaced

- removed lines 9, added lines 9; words 85 → 82
- **lost:** the ×2, But, answered, bought, earlier, first, leaving, only, stays, text
- **gained:** Leaving, an, answer, both, buy, need, stands, would

## `770ffcb` Readable: §14.4, §2.2 — the R-SER-04 withdrawal Note moved from §14.4 to §2.2; R-SER-04 listed

- removed lines 4, added lines 3; words 22 → 18
- **lost:** 2 ×2, Identifier, earlier, it, per, permanently, subsection, this
- **gained:** 14, 4, One, identifier, once

## `586e412` Readable: §14.4 — the layout Rationale: maintainer's edit reviewed; ADR-0038's epigram in its own terms

- removed lines 3, added lines 5; words 30 → 47
- **lost:** a, as, dishonest, format, gets, honest, inexpressible, makes, one, plane, that
- **gained:** would ×2, 0, 1, Barred, an, and, be, bool, bytes, channel, consumer, conversion, declared, erased, every, from, in, inherit, instead, int8, interleaved, label, layers, layout, same, untyped, with

## `a183cf6` Readable: §15.1 — maintainer's edit, reviewed: entries grouped in channel-major order; R-IDX-01 listed

- removed lines 7, added lines 6; words 62 → 65
- **lost:** group
- **gained:** are, grouped, in, order

## `39c2ff5` Readable: §15.4 — a Rationale for segments: why, and that a writer has no choice in them

- removed lines 0, added lines 16; words 0 → 182
- **lost:** (none)
- **gained:** the ×11, a ×10, CRC ×8, and ×8, array ×5, one ×5, at ×4, entry ×4, index ×4, reader ×4, MiB ×3, layer ×3, over ×3, segment ×3, single ×3, to ×3, use ×3, whole ×3, 1 ×2, Segments ×2, an ×2, any ×2, entries ×2, is ×2, its ×2, million ×2, not ×2, or ×2, per ×2, see ×2, under ×2, would ×2, writer ×2, 19, 190, 2, 25, 2¹⁶, 536, 65, 8, A, Rationale, Under, With, about, alone, are, before, both, bound, declines, duty, entire, every, fetch, fetches, follow, from, full, has, holding, index_encoding, laid, more, most, naive, never, nothing, oblige, of, only, option, out, outgrows, partial, plus, ranges, record, remote, scale, segmentation, shows, so, takes, ten, than, that, they, this, tile, tiles, verifies, verify, way, what, when, writer's

## `03b5329` Readable: §16.2 — the slab-scope Note made a Rationale that says what slabs are for

- removed lines 11, added lines 19; words 105 → 207
- **lost:** are ×2, Note, Rectangular, With, guarantees, job, need, only, property, slabs
- **gained:** a ×7, the ×5, one ×4, by ×3, can ×3, index ×3, it ×3, run ×3, A ×2, adds ×2, and ×2, as ×2, direct ×2, in ×2, is ×2, per ×2, reader ×2, that ×2, A_slab, I, O, Rationale, So, advance, alignment, alone, always, arithmetic, at, before, buffer, business, but, byte, checkable, contiguity, contiguous, declaration, detect, does, each, entries, entry, fetch, fetched, for, has, holding, holds, however, issue, itself, left, make, many, needed, planner, promise, promises, range, read, rectangular, requests, run's, single, size, sizes, slab's, start, stored, their, thing, tile, tiles, verifier, wants, whatever, when, with, within

## `0c3ab26` Readable: §17.4 — re-wrapped, no word changed; §16 and §17 added to the stretch list

- removed lines 16, added lines 14; words 159 → 159
- **lost:** (none)
- **gained:** (none)

## Whole range, every commit's hunks pooled

- **lost:** may ×6, residue ×6, claimant ×2, makes ×2, second ×2, values ×2, But, Bytes, C, Column, Field, Identifier, Note, Rectangular, Residue, Spatial, There, adjacent, all, answered, be, bought, carried, carrying, completes, content, covering, creation, dishonest, do, earlier, ecosystems, either, emitted, enters, first, fixes, forbids, format, generation's, governs, group, guarantees, honest, included, inexpressible, job, layer's, leaving, mapping, names, normatively, ordinals, other, past, permanently, plane, property, qualify, raises, reaching, reusing, rewrite, says, slabs, states, subsection, supersedes, text, traversal, violates, walk, write, writing
- **gained:** the ×42, is ×27, it ×25, and ×23, a ×17, that ×15, to ×14, R ×13, bytes ×13, file ×12, committed ×11, state ×11, LIF ×10, as ×10, in ×10, its ×10, one ×10, A ×9, CRC ×8, index ×8, last ×8, an ×7, 1 ×6, leaves ×6, length ×6, not ×6, reader ×6, array ×5, entry ×5, every ×5, has ×5, tile ×5, with ×5, would ×5, 09 ×4, In ×4, Its ×4, byte ×4, can ×4, layer ×4, no ×4, ordinal ×4, record ×4, single ×4, so ×4, tool ×4, truncates ×4, updater ×4, when ×4, 06 ×3, 9 ×3, MiB ×3, The ×3, adds ×3, after ×3, are ×3, at ×3, both ×3, but ×3, by ×3, carries ×3, complete ×3, each ×3, entries ×3, for ×3, order ×3, over ×3, per ×3, remaining ×3, run ×3, segment ×3, through ×3, use ×3, whole ×3, writer ×3, 's ×2, 01 ×2, 02 ×2, 14 ×2, 3 ×2, 5 ×2, 6 ×2, It ×2, MUST ×2, Rationale ×2, Segments ×2, Under ×2, above ×2, alone ×2, any ×2, before ×2, below ×2, binds ×2, bound ×2, candidate's ×2, claimed ×2, direct ×2, equal ×2, fetch ×2, holds ×2, into ×2, million ×2, of ×2, operation ×2, or ×2, own ×2, performs ×2, physical ×2, positions ×2, range ×2, ranges ×2, re ×2, read ×2, runs ×2, see ×2, spatial ×2, stays ×2, step ×2, steps ×2, sub ×2, than ×2, travels ×2, truncation ×2, under ×2, verifies ×2, within ×2, 0, 05, 08, 19, 190, 2, 20, 25, 2¹⁶, 4, 4's, 536, 65, 7, 8, A_slab, All, Barred, Because, CNF, CNT, Every, Growth, I, Leaving, NOT, No, O, Readers, SER, So, TARN, Take, That, They, This, What, advance, again, alignment, allowed, always, answer, appends, arithmetic, belong, beyond, block's, bool, buffer, business, buy, case, cautions, certifying, change, channel, cheap, claiming, column, conforming, consumer, contiguity, contiguous, conversion, covers, created, decides, declaration, declared, declines, default, derives, describe, detect, does, duty, ecosystem, else, emits, entire, erased, established, extent, extra, fall, fetched, fetches, field, five, follow, following, forced, forward, free, from, full, generation, grouped, holding, how, however, identifier, includes, index_encoding, inherit, instead, int8, interleaved, issue, itself, label, laid, latent, layers, layout, leave, left, linearization, live, make, many, maps, modifies, modify, more, most, naive, need, needed, never, nothing, notion, oblige, office, once, option, out, outgrows, output, partial, partitions, path, planner, plus, position, present, probe, promise, promised, promises, provides, rather, reach, reached, reads, rectangular, region, remote, removes, reports, requests, requires, rest, resulting, right, rises, rollback, run's, same, say, scale, screen, section's, segmentation, short, shows, since, sit, size, sizes, slab's, slack, stands, start, state's, stored, structures, such, superseded, supports, takes, ten, their, them, there, they, thing, though, tiles, together, too, truncate, truncating, type, untyped, value, verification, verifier, verifier's, verify, violate, violation, wants, was, well, whatever, where, which, writer's, writes, yield

## Whole range as one diff (`git diff 58d3201^ 0c3ab26`)

- removed lines 288, added lines 343
- **lost:** may ×6, residue ×6, claimant ×2, makes ×2, second ×2, values ×2, But, Bytes, C, Column, Field, Identifier, Note, Rectangular, Residue, Spatial, There, adjacent, all, answered, be, bought, carried, carrying, completes, content, covering, creation, dishonest, do, earlier, ecosystems, either, emitted, enters, first, fixes, forbids, format, generation's, governs, group, guarantees, honest, included, inexpressible, job, layer's, leaving, mapping, names, normatively, ordinals, other, past, permanently, plane, property, qualify, raises, reaching, reusing, rewrite, says, slabs, states, subsection, supersedes, text, traversal, violates, walk, write, writing
- **gained:** the ×42, is ×27, it ×25, and ×23, a ×17, that ×15, to ×14, R ×13, bytes ×13, file ×12, committed ×11, state ×11, LIF ×10, as ×10, in ×10, its ×10, one ×10, A ×9, CRC ×8, index ×8, last ×8, an ×7, 1 ×6, leaves ×6, length ×6, not ×6, reader ×6, array ×5, entry ×5, every ×5, has ×5, tile ×5, with ×5, would ×5, 09 ×4, In ×4, Its ×4, byte ×4, can ×4, layer ×4, no ×4, ordinal ×4, record ×4, single ×4, so ×4, tool ×4, truncates ×4, updater ×4, when ×4, 06 ×3, 9 ×3, MiB ×3, The ×3, adds ×3, after ×3, are ×3, at ×3, both ×3, but ×3, by ×3, carries ×3, complete ×3, each ×3, entries ×3, for ×3, order ×3, over ×3, per ×3, remaining ×3, run ×3, segment ×3, through ×3, use ×3, whole ×3, writer ×3, 's ×2, 01 ×2, 02 ×2, 14 ×2, 3 ×2, 5 ×2, 6 ×2, It ×2, MUST ×2, Rationale ×2, Segments ×2, Under ×2, above ×2, alone ×2, any ×2, before ×2, below ×2, binds ×2, bound ×2, candidate's ×2, claimed ×2, direct ×2, equal ×2, fetch ×2, holds ×2, into ×2, million ×2, of ×2, operation ×2, or ×2, own ×2, performs ×2, physical ×2, positions ×2, range ×2, ranges ×2, re ×2, read ×2, runs ×2, see ×2, spatial ×2, stays ×2, step ×2, steps ×2, sub ×2, than ×2, travels ×2, truncation ×2, under ×2, verifies ×2, within ×2, 0, 05, 08, 19, 190, 2, 20, 25, 2¹⁶, 4, 4's, 536, 65, 7, 8, A_slab, All, Barred, Because, CNF, CNT, Every, Growth, I, Leaving, NOT, No, O, Readers, SER, So, TARN, Take, That, They, This, What, advance, again, alignment, allowed, always, answer, appends, arithmetic, belong, beyond, block's, bool, buffer, business, buy, case, cautions, certifying, change, channel, cheap, claiming, column, conforming, consumer, contiguity, contiguous, conversion, covers, created, decides, declaration, declared, declines, default, derives, describe, detect, does, duty, ecosystem, else, emits, entire, erased, established, extent, extra, fall, fetched, fetches, field, five, follow, following, forced, forward, free, from, full, generation, grouped, holding, how, however, identifier, includes, index_encoding, inherit, instead, int8, interleaved, issue, itself, label, laid, latent, layers, layout, leave, left, linearization, live, make, many, maps, modifies, modify, more, most, naive, need, needed, never, nothing, notion, oblige, office, once, option, out, outgrows, output, partial, partitions, path, planner, plus, position, present, probe, promise, promised, promises, provides, rather, reach, reached, reads, rectangular, region, remote, removes, reports, requests, requires, rest, resulting, right, rises, rollback, run's, same, say, scale, screen, section's, segmentation, short, shows, since, sit, size, sizes, slab's, slack, stands, start, state's, stored, structures, such, superseded, supports, takes, ten, their, them, there, they, thing, though, tiles, together, too, truncate, truncating, type, untyped, value, verification, verifier, verifier's, verify, violate, violation, wants, was, well, whatever, where, which, writer's, writes, yield

## Hand-check, 2026-10-20 (the driver, before round 3's launch)

This range is the maintainer's read-through, which changed words on purpose, so the accounting is not round 2's connective list: every commit's lost and gained words are read against its edit-log entry (the "Edits" paragraph and, where the entry carries one, the "Word-level diff" line, with the before and after texts the entry quotes). Every lost or gained word above is accounted for; none is a transcription defect; nothing is restored. Three notes for the findings file follow the list.

- **`58d3201` (§9.1–§9.2).** "Bytes" → "All bytes", the dash aside "with", "and every" → ". Every" (the split), "(a rewrite, §20.5)" → "(§20.5)", the steps re-set at line starts with no word changed; the creation paragraph's "whose … writing … There being" → "the block's … Because there is": exactly the entry's line ("the splits' connectives and capitals, 'a rewrite' and 'writing' lost, 'with', 'block's' and 'Because' gained, nothing else").
- **`1df7b0d` (§9.2, the strict-increase Note).** The ten lost and nine gained words are the entry's word-level diff line verbatim ("it" twice: "before it; it is" and "as the Note above reads it").
- **`48e65f4` (§9.2, the crash Example's lead-in).** "in" ×2 → "In" ×3 with "it is" ×2 and "In the following": the colon list made three sentences, as quoted.
- **`44f113d` (§9.2–§9.3).** "never" → "not"; "one" → "generation"; the first Note's "is what makes it checkable: no" → the citation sentence ("R", "LIF", "CNT", "01", "02", "06", "'s", "steps", "1", "3", "5", "forced", "performs", "promised", "beside", "them", "yield", "derives", "conforming", "writer", "rather", "than") and "No" as the sentence of its own; "makes" and "what" are the quoted before-text's.
- **`8b1eefe` (§9.4–§9.5).** "completes" → "is completed"; "One writer at a time, … this" → "TARN supports … but only one writer at a time. This"; the Note's three "residue" phrasings → "The case in which extra bytes are present in the file beyond the committed file length", "such bytes", "those bytes violate" (so "past", "a", "commit", "violates" lost; "bytes", "file", "beyond", "committed", "length", "extra", "present", "case", "which", "those", "violate" gained): the entry's quoted texts.
- **`64b6e5e` (§7.2, §7.4).** "residue" ×4 → "bytes remaining after the last complete record / sub-record" ×3 and "bytes remaining" in the Example: the entry's three items; every keyword clause verbatim.
- **`a4ac2d2` (the ADR-0134 port).** Nothing lost; every gained word is one of the four insertions. The `[R-LIF-09]` paragraph is unlisted and the inventory passes, so it is verbatim A's; the §2.3, §20.1 and Appendix H sentences are found whole in `main`'s spec by whitespace-normalised search (1 hit each in A and in B).
- **`2d3e790` (the erratum).** "that" → "the candidate's".
- **`66b0f01` (§9.7, the claimants paragraph).** The gloss's words ("structures", "partitions", "live", "committed", "state", "into", "each", "claiming", "bytes", "belong", "rest", "being", "slack", "5", "2" for §5.2, "They", "are"); "is not a claimant of its own: … which is the claimant covering them, so reaching … is traversal, not a second claim on those bytes" → "does not claim bytes in its own right. Its … and the directory region is the claimant that covers them, so a record reached … adds no claimed range of its own"; "addresses that layer's tile-index region … so the region enters the walk once … and is not a second claimant beside it" → "A layer's tile-index region is the extent that … so it is claimed once … and not again as a region": the entry's three quoted edits; every pointer kept.
- **`f96eb0b` (§10).** "spaces, … and" → "spaces are … but".
- **`dc66fc9` (§11.1, the growth Rationale).** The six "may"s rewritten around ("is allowed to", "is extended", "is declared", "can be re-declared", "grow and never shrink", "names change"); "§20.3 states normatively, and governs, what … may do to" → "What … is allowed to change on … is §20.3 step 4's to say. In short:"; "one or the other in a commit" → "not both in one commit"; "the declarations it produces" → "the resulting declarations"; "is fixed" → "stays fixed"; "the generation the commit supersedes may be" → "the superseded generation can be"; "does not qualify" → "though not"; "so does one that raises … the product holding at 0 and the index empty either way" → "the same holds when one grid count rises … since the product stays 0 and the index stays empty"; "the index content — … moves them — so the layer's whole tile-index region is re-emitted (…), the growth that raises a zero-extent layer's **only remaining** zero grid count included" → "the index: … moves them, so the commit re-emits the layer's whole tile-index region (…). That includes the growth that raises the last zero grid count of a zero-extent layer": the entry's fact list, item by item. Two wordings the entry's fact list does not name, both inside the approved rewrite: "Growth is cheap where it changes no grid count" is a new topic sentence (the entry quotes it; "cheap" occurs in A only in §21.9's Note and §22), and "already stored tiles" reads "already stored a tile", the quantifier §20.3 step 4 uses ("stores a tile"). For the round to grade, as the handoff expects of this block.
- **`0b9ed09` (§11.2).** "whose" lost, "its" and "and" gained: the entry's line.
- **`0db63fe` (§11.4, the Note).** "fixes the mapping from" → "decides only how … maps"; "it says nothing about" → "It carries no notion of"; "carried" → "travels"; "Column-major ecosystems (…) write" → "A column-major ecosystem such as … gets zero-copy writes"; "the same convention their" → "which is the convention its": the quoted after-text.
- **`c21a48d` (§11.4, the Example).** "Spatial ordinals:" and the three arrows → "Under linearization 1, … has spatial ordinal … has ordinal … whose spatial ordinal is … whose in-tile ordinal is"; "carrying" → "that carries"; every figure kept, as the entry re-derives.
- **`3ed24c3` (§12.2).** "The field's values:" → "The type field's values fall into five ranges:".
- **`fd87472` (§12.3, §13.1).** "with … of" in the Example; "that" in `[R-TYP-10]`. **A third hunk the entry does not record, punctuation only** (so no word in the counts): §13.3's `[R-TYP-08]` paragraph, "MUST return, for each channel the tile carries, that channel's fill" → "MUST return (for each channel the tile carries) that channel's fill". Note 1 below.
- **`58dd3bb` (§13.2).** The one appended sentence ("Readers need not screen value bytes for it (§14.2, `[R-SER-08]`)").
- **`b96560c` (§14.1, the bullets).** "exactly the values of channel c" → "one channel, c, … and nothing else"; "all C channels" → "every channel"; "adjacent in declared channel order" → the order clause and "sit together"; "runs through", "in in-tile order" ×2, "within each position": the entry's quoted bullets.
- **`ff7bac9` (§14.1, the layout field).** "Field values: 0 is invalid;" moved after the defined values as "0 is invalid, and"; "for the field" gained.
- **`52dbc95` (§14.2, the Rationale).** "the earlier text answered only the first" → "both need an answer"; "stays" → "stands"; "But leaving … bought" → "Leaving … would buy": the entry's line.
- **`770ffcb` (§14.4 → §2.2, the Note moved).** "Identifier …, which earlier governed this subsection, is withdrawn; per §2.2 it is permanently retired and never reassigned" → "One identifier is retired: …, which once governed §14.4, is withdrawn and never reassigned": the entry's quoted before and after texts. Note 2 below.
- **`586e412` (§14.4, the Rationale).** "as a planar plane" → "in planar layout"; the epigram ("a format that makes the honest type inexpressible gets the dishonest one") → its content ("Barred from interleaved layers, a bool channel would be declared int8 instead, the same bytes with the type label erased, and every consumer would inherit an untyped 0/1 conversion"): the entry's quoted sentences.
- **`a183cf6` (§15.1).** "group channel-major" → "are grouped in channel-major order"; the opening re-wrapped with no word changed.
- **`39c2ff5` (§15.4, the Rationale added).** Nothing lost; the Rationale's words gained. Its figures re-derived: 10⁶ × 20 B = 19.07 MiB, 10⁷ × 20 B = 190.7 MiB, 2¹⁶ × 20 B = 1.25 MiB, as the entry derives them from the section's Example and ADR-0024.
- **`03b5329` (§16.2, the Note made a Rationale).** Lost: the label ("Note", "what slabs are, and are not") and the five kept facts' old wording ("guarantees" → "promises one thing", "job" → "the linearization field's", "Rectangular-window locality is therefore not a slab property" → "a slab does not by itself make a rectangular window contiguous; that locality", "contiguity-only" → "contiguity alone", "With" → "with", "alignment need" → "alignment is needed"); gained: the motivations the entry lists (the one-range fetch, the planner's buffer and direct read, arithmetic detection against the declaration's checkable promise, A_slab's alignment at a run's start) and "within a run" qualifying contiguity. New explanatory prose, for the round.
- **`0c3ab26` (§17.4).** Nothing lost, nothing gained: the re-wrap.

The range pooled commit by commit and the range as one diff agree word for word (checked mechanically below), so no word moved between commits hides a loss.

**Notes for the findings file.**

1. **An unlogged punctuation edit in a listed rule paragraph** (`fd87472`, §13.3, `[R-TYP-08]`): commas → parentheses around "for each channel the tile carries"; no word changed; the same statement. `R-TYP-08` has been listed since the §13 spruce-up (`db2b575`), whose reason line reads "the MUST verbatim", true of the words and no longer of the punctuation; the inventory cannot see it. The commit is a batch of the maintainer's hand edits reviewed under procedure 2a, and the entry records two hunks of three. Not a word-diff repair, so nothing is committed before the launch; the entry's amendment and the reason line go with the round's findings commit, and the maintainer is told.
2. **`770ffcb`'s summary sentence understates its own quotations**: "the same fact in the same words but for 'per §2.2'", where the committed text (the entry's quoted after-text) also drops "permanently", reads "once" for "earlier" and "§14.4" for "this subsection", and opens "One identifier is retired:". §2.2's rule two paragraphs above says "a withdrawn requirement leaves its identifier permanently retired", identical in both editions, so the permanence stands where the Note now sits. Accounted; no loss.
3. **`dc66fc9`'s two unnamed wordings** (above): the new topic sentence and the quantifier. Explanatory prose inside a Rationale the round grades.
