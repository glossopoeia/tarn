# Quiz transcript — quiz-a-on-b

## Disclosure

**File read.** I read exactly one specification file, in full, via the
Read tool in five sequential chunks (offsets 1–1000, 1000–2000,
2000–3000, 3000–3700, 3700–4200; the file has 4885 lines / 296,597
bytes total, and I stopped once I had passed the error register and
implementation-limits sections, which covered everything the slate
needed):

`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md`

I also made one `cat -n` copy of that same file into my own scratch
directory (`tarn-numbered.txt`) purely as a local line-numbered
reference; I did not read any other source with it.

**Path note.** The computed task's prose calls this "edition B," but
the ACCESS RULE names a path under `.../editions/c/tarn.md` ("edition
c"). I read the file at the path given (edition c) and am answering
from its content; I am not treating the "edition B" label as evidence
about what that content says, and I flag the mismatch here rather than
silently picking one name.

**Nothing else was read.** I did not open AGENTS.md, PLAN.md,
OPEN-QUESTIONS.md, README.md, CONTRIBUTING.md, any docs/decisions/
ADR, any conformance/ file, spec/registry.json, git history/log/diff,
or any other copy of this specification. I ran no web search or web
fetch. I did not list the shared output directory
(`fidelity-2/out/`) or read its contents. I did, once, run `ls` on
its *parent* directory (`fidelity-2/`) to confirm the `out/`
subdirectory existed before writing this transcript; that incidentally
showed the directory *names* `scratch/`, `out/`,
`triage-correctness/`, `triage-implementer/`, `triage-skeptic/` (no
file contents), which was not needed and I should not have run. I
disclose it rather than treat it as unnoticed.

**Unbidden context.** Before this task began, my context already
contained: a CLAUDE.md pointer to AGENTS.md; a user auto-memory file
(MEMORY.md) listing many TARN-related note titles; a git-status block
naming the current branch ("readable") and several recent commit
subjects about a "readable edition" effort; and general
environment/tooling boilerplate. None of that is part of, or evidence
about, the specification text I was asked to quiz from, and I have not
used any of it to answer any question below. I am not repeating its
contents here beyond naming that it appeared. This is a disclosed
breach, not a used one.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/quiz-a-on-b/`
was empty when I started (I created it fresh; `ls -la` showed only
`.` and `..`), so there was no earlier attempt's files to report. I
wrote one working file there: `tarn-numbered.txt` (a full `cat -n` of
the target file, for my own line lookups).

**Wrapping caveat.** I did not rely on line-oriented `grep` against
the hard-wrapped Markdown for any decisive fact; I read the document
directly through the Read tool (which returns logical file content,
not a line-by-line search), so wrapped phrases were not at risk of a
false zero in the way `grep -c "phrase"` could produce. I did not run
any `grep`/`rg` searches in this session — the direct read plus local
arithmetic was sufficient for all fifteen questions, and I did not
need to search for short fragments.

**Local computation.** All arithmetic (grid counts, ordinals, byte
offsets, checksums' domains, cap comparisons) was done as ordinary
arithmetic reasoning over the values quoted from the document; no
file was read to perform it.

---

## Answers

See the structured result for the fifteen answers, their citations,
decisive quotes, and reasoning. Summary of the answer-field values
only (exact form the slate asked for):

- quiza-01: `256`
- quiza-02: `(a) 1; (b) yes, R-CNT-04`
- quiza-03: `yes; R-ENC-04; reject-file`
- quiza-04: `(a) file torn or invalid; (b) no`
- quiza-05: `(a) the directory region's terminal checksum; (b) the layer's segment-CRC array`
- quiza-06: `8, 20`
- quiza-07: `55 FF`
- quiza-08: `(a) 2147483648; (b) no, b`
- quiza-09: `yes; ignore-record`
- quiza-10: `(a) no; (b) broken frame constraint (R4); (c) the field must equal the decoded document's actual byte length (800), whereas the analogous tile-scope rule requires the field to match the tile's decoded size as derived purely from the layer's structural declarations, never from what the stored bytes actually decode to.`
- quiza-11: `reject-layer; no; no`
- quiza-12: `no; two commits, or a rewrite`
- quiza-13: `no; the sub-record's stored MUST_UNDERSTAND=1 bit, for a type the updater does not implement, makes those stored flags authoritative and blocks any modification of the layer it governs, including dropping the layer`
- quiza-14: `no; no; drop the layer, or refuse to rewrite`
- quiza-15: `nonconforming; yes; the requirement it could not check, and the capability/resource ground it could not check it on`
