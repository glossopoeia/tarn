#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""Editorial check: prove a spec change altered no normative content.

CONTRIBUTING requires every change to normative text to cite the ADR that
governs it. That is right for decisions and wrong for readability work, which
forced a choice between ADRs recording no decision and an unwritten exception.
ADR-0104 takes a third option: authorise the class once, and replace the
per-change ADR with a check that *proves* a change was editorial rather than
asserting it.

    tarn_editorial.py                  # working tree against HEAD
    tarn_editorial.py --base <rev>     # against any revision
    tarn_editorial.py --rev <commit>   # what that commit changed
    tarn_editorial.py --selftest       # verdicts against known commits
    tarn_editorial.py --strict         # placement counts as content
    tarn_editorial.py -v               # show the differing text

WHY THE BURDEN IS ON THE TOOL

"This edit doesn't change the meaning" is the claim this project has got wrong
more often than any other. In one week: a gloss reworded from an accurate form
into a false one; a pronoun disambiguated in a register row and left standing in
the rule the row restates; a Rationale re-keyed onto a quantity that does not
decide the question; and the single word *last*, which five independent readers
found ambiguous at once. Every one was offered as a clarification. So the
author's judgement about their own edit is the wrong instrument — and it is the
only instrument a per-change ADR supplies, since an ADR saying "this is
editorial" records the same unchecked claim at greater length.

HOW IT COMPARES, AND WHY NOT BY REQUIREMENT ID

An earlier version keyed normative text by the `[R-XXX-NN]` identifier ending
each requirement. That was wrong, and wrong in the dangerous direction. The
identifiers are not only definitions: they appear as citations too, in
parentheses, as possessives, and in ranges — 265 parenthetical and 37 possessive
occurrences against 152 that end a line. Worse, the document is hard-wrapped, so
a requirement's closing identifier routinely shares a line with the *next*
requirement's opening words, and no punctuation rule separates the two cases.
Keying a dictionary by identifier meant the last citation in document order
silently overwrote the definition. Run against ADR-0102's commit, that version
found one of five changed passages and attributed it to two requirements defined
in other sections — and returned CONTENT only because a citing paragraph
happened to change in the same commit.

This version needs no attribution. It compares **the normative prose of each
section, concatenated and whitespace-normalised**:

  · Blockquote lines are excluded — [R-CNF-01] puts Note, Rationale and Example
    outside normative text, and they are 18.5% of the document.
  · Table rows are excluded from the prose and compared separately, exactly.
  · Fenced code blocks are excluded.

Because a whole section's prose is one string, re-wrapping a paragraph, splitting
one paragraph into two, and merging two into one are all invisible — which is
what makes the check useful for readability work. Because the comparison is
per-section, text that moves between sections is caught.

THREE VERDICTS

  EDITORIAL  Every section's normative prose is unchanged, and so is every
             table row. Commit with an `editorial:` subject and no ADR.

  PLACEMENT  The document's normative sentences are exactly the same multiset,
             but some sit in a different section. Allowed on the same terms, and
             reported separately because placement is not content-neutral here:
             [R-ENC-04] reaches quantities designated by "the section that
             defines" them, §2.4 assigns owning scope by structure, and §21.1
             subordinates a register row to the rule it cites. The tool names
             every sentence that moved, and any requirement identifier inside it.

  CONTENT    Normative prose or a table cell changed. Needs an ADR. The tool
             prints the differing sentences so the author can see at once
             whether it is substance or markup.

KNOWN LIMITS, STATED SO THEY ARE NOT DISCOVERED LATER

It compares text, so it cannot see that a moved rule reads differently in its
new neighbourhood — that is what the PLACEMENT checklist is for, and it is
advisory. It cannot see a normative sentence reordered *within* one section.
It treats any table cell change as CONTENT even when only markup moved, which
over-flags rather than under-flags, deliberately. And it says nothing about
whether new wording is better — only that the old meaning survived.

Exit status is 1 on CONTENT, and on PLACEMENT under --strict.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = "spec/tarn.md"

REQ = re.compile(r"\[(R-[A-Z]{3}-\d{2})\]")
HEADING = re.compile(r"^(#{2,6})\s+(.*)$")
SECNUM = re.compile(r"^((?:\d+\.)*\d+|Appendix\s+[A-Z])")
SENTENCE = re.compile(r"(?<=[.:;])\s+")
KEYWORD = re.compile(
    r"\b(MUST NOT|SHALL NOT|SHOULD NOT|MUST|SHALL|SHOULD|MAY|REQUIRED|RECOMMENDED|OPTIONAL)\b"
)
LOCATION_SENSITIVE = re.compile(
    r"designat|declaration-derived|owning scope|the section that|this section", re.I
)


def git(*args: str) -> str:
    r = subprocess.run(
        ["git", "-C", str(REPO), *args], capture_output=True, text=True, check=False
    )
    return r.stdout


def norm(s: str) -> str:
    return " ".join(s.split())


def parse(text: str) -> tuple[dict[str, str], Counter]:
    """-> (section -> normalised normative prose, table rows as a multiset)"""
    prose: dict[str, list[str]] = {}
    tables: Counter = Counter()
    section = "(front matter)"
    fenced = False

    for line in text.split("\n"):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue

        h = HEADING.match(line)
        if h:
            title = h.group(2).strip()
            m = SECNUM.match(title)
            section = m.group(1) if m else title
            continue

        stripped = line.lstrip()
        if stripped.startswith(">"):        # non-normative, [R-CNF-01]
            continue
        if stripped.startswith("|"):        # compared separately, exactly
            cells = tuple(norm(c) for c in line.strip().strip("|").split("|"))
            if all(set(c) <= set("-: ") for c in cells):
                continue                    # markdown rule row
            tables[cells] += 1
            continue

        prose.setdefault(section, []).append(line)

    return {k: norm(" ".join(v)) for k, v in prose.items()}, tables


def sentences(section_prose: dict[str, str]) -> Counter:
    out: Counter = Counter()
    for text in section_prose.values():
        for s in SENTENCE.split(text):
            s = s.strip()
            if s:
                out[s] += 1
    return out


def sentences_by_section(section_prose: dict[str, str]) -> dict[str, str]:
    """sentence -> the section it sits in (last wins; only used for reporting)"""
    where = {}
    for sec, text in section_prose.items():
        for s in SENTENCE.split(text):
            s = s.strip()
            if s:
                where[s] = sec
    return where


def report_diff(before: str, after: str, limit: int = 3) -> None:
    b = [s.strip() for s in SENTENCE.split(before) if s.strip()]
    a = [s.strip() for s in SENTENCE.split(after) if s.strip()]
    gone = [s for s in b if s not in set(a)]
    new = [s for s in a if s not in set(b)]
    for s in gone[:limit]:
        print(f"      - {s[:220]}")
    for s in new[:limit]:
        print(f"      + {s[:220]}")
    extra = max(len(gone) - limit, 0) + max(len(new) - limit, 0)
    if extra:
        print(f"      … {extra} more sentence(s)")


def compare(before: str, after: str, strict: bool, verbose: bool) -> int:
    pb, tb = parse(before)
    pa, ta = parse(after)

    sb, sa = sentences(pb), sentences(pa)
    ids_b = Counter(REQ.findall(before))
    ids_a = Counter(REQ.findall(after))

    changed_sections = sorted(
        s for s in set(pb) | set(pa) if pb.get(s, "") != pa.get(s, "")
    )
    tbl_gone = list((tb - ta).elements())
    tbl_new = list((ta - tb).elements())

    print(f"  {len(pa)} section(s) of normative prose; {sum(ta.values())} table row(s)")
    print(f"  {sum(sa.values())} normative sentence(s); {len(set(ids_a))} requirement id(s)")
    print()

    if not changed_sections and not tbl_gone and not tbl_new:
        print("EDITORIAL — no normative prose changed and no table row changed.")
        print("No ADR required (ADR-0104). Commit with an `editorial:` subject.")
        return 0

    # same sentences everywhere, different sections => pure placement
    placement = (sb == sa) and not tbl_gone and not tbl_new

    if tbl_gone or tbl_new:
        print(f"TABLE ROWS CHANGED: {len(tbl_gone)} removed, {len(tbl_new)} added")
        for r in tbl_gone[:5]:
            print(f"  - {' | '.join(r)[:170]}")
        for r in tbl_new[:5]:
            print(f"  + {' | '.join(r)[:170]}")
        print()

    if set(ids_b) != set(ids_a):
        print("REQUIREMENT IDS ENTERED OR LEFT THE DOCUMENT:")
        for i in sorted(set(ids_a) - set(ids_b)):
            print(f"  + {i}")
        for i in sorted(set(ids_b) - set(ids_a)):
            print(f"  - {i}")
        print()

    if placement:
        wb, wa = sentences_by_section(pb), sentences_by_section(pa)
        moved = [(s, wb[s], wa[s]) for s in wa if s in wb and wb[s] != wa[s]]
        print("NORMATIVE TEXT MOVED, UNCHANGED:")
        for s, frm, to in moved[:20]:
            ids = ", ".join(sorted(set(REQ.findall(s)))) or "—"
            hot = "  <-- location-sensitive wording" if LOCATION_SENSITIVE.search(s) else ""
            print(f"  → §{frm} → §{to}  [{ids}]{hot}")
            print(f"      {s[:190]}")
        if len(moved) > 20:
            print(f"  … {len(moved) - 20} more")
        print()
        print("  Placement is not content-neutral here. Before accepting, check:")
        print("    · [R-ENC-04] reaches quantities designated by the section defining them")
        print("    · §2.4 assigns owning scope by structure")
        print("    · §21.1 subordinates a register row to the rule it cites")
        print()
        print("PLACEMENT — no normative prose changed; some of it moved.")
        print("Allowed without an ADR under ADR-0104, once those checks are made.")
        print("Commit with an `editorial:` subject naming what moved and why.")
        return 1 if strict else 0

    if changed_sections:
        print("NORMATIVE PROSE CHANGED:")
        for s in changed_sections:
            b, a = pb.get(s, ""), pa.get(s, "")
            kb, ka = Counter(KEYWORD.findall(b)), Counter(KEYWORD.findall(a))
            print(f"  ~ §{s}")
            if kb != ka:
                print(f"      BCP 14 keywords: {dict(kb - ka)} removed, {dict(ka - kb)} added")
            if verbose:
                report_diff(b, a)
            else:
                report_diff(b, a, limit=1)
        print()

    print("CONTENT — this changes normative text and needs an ADR (CONTRIBUTING,")
    print("AGENTS.md rule 2). If the diff above is only markup, restore the markup")
    print("and re-run, or record the judgement in the ADR.")
    return 1


CASES = [
    # (commit, expected verdict, why this commit's answer is known independently)
    ("830f08e", "CONTENT", "ADR-0102 rewrote [R-ENC-04] and four other passages"),
    ("2153722", "CONTENT", "ADR-0103 changed §17's preamble, [R-COD-04], Appendix G"),
    ("2cb7cd3", "CONTENT", "ADR-0099 changed [R-SLB-03]'s contiguity clause"),
    ("c8e593a", "EDITORIAL", "ADR-0101 changed only §17.2's Note — every changed "
                             "line begins '>', so [R-CNF-01] puts all of it outside "
                             "normative text. An ADR was written that this rule "
                             "would not have required"),
]


def verdict(before: str, after: str) -> str:
    pb, tb = parse(before)
    pa, ta = parse(after)
    same_prose = all(pb.get(s, "") == pa.get(s, "") for s in set(pb) | set(pa))
    if same_prose and tb == ta:
        return "EDITORIAL"
    if sentences(pb) == sentences(pa) and tb == ta:
        return "PLACEMENT"
    return "CONTENT"


def synthetic(spec: str) -> list[tuple[str, str, str]]:
    """Cases built by mutating the current document, so all three verdicts are
    exercised. A suite of CONTENT-only cases would pass for a tool that always
    said CONTENT — which is the shape of the mistake this file exists to avoid.
    """
    lines = spec.split("\n")

    def find_prose(section_marker: str, skip: int = 0) -> int:
        """index of a normative prose line inside the named section"""
        seen = False
        for i, l in enumerate(lines):
            if l.startswith(section_marker):
                seen = True
                continue
            if seen and l.strip() and not l.lstrip().startswith((">", "|", "#", "`")):
                if skip:
                    skip -= 1
                    continue
                return i
            if seen and l.startswith("#### ") and not l.startswith(section_marker):
                break
        return -1

    out = []

    # 1. re-wrap: join two adjacent prose lines. Whitespace only.
    i = find_prose("#### 11.3")
    if i > 0 and lines[i + 1].strip():
        w = lines[:]
        w[i : i + 2] = [w[i] + " " + w[i + 1].strip()]
        out.append(("re-wrap two lines in §11.3", "EDITORIAL", "\n".join(w)))

    # 2. split a paragraph in two. Structure only.
    i = find_prose("#### 11.3")
    if i > 0 and lines[i + 1].strip():
        w = lines[:]
        w.insert(i + 1, "")
        out.append(("split a §11.3 paragraph", "EDITORIAL", "\n".join(w)))

    # 3. edit a blockquote. Non-normative under [R-CNF-01].
    for i, l in enumerate(lines):
        if l.startswith("> ") and len(l) > 30:
            w = lines[:]
            w[i] = l + " Wording added to a Note."
            out.append(("add a sentence to a Note", "EDITORIAL", "\n".join(w)))
            break

    # 4. change one word of normative prose.
    i = find_prose("#### 11.3")
    if i > 0 and " the " in lines[i]:
        w = lines[:]
        w[i] = lines[i].replace(" the ", " each ", 1)
        out.append(("one word in §11.3's normative prose", "CONTENT", "\n".join(w)))

    # 5. move a normative sentence to another section.
    src = find_prose("#### 11.3")
    dst = find_prose("#### 11.4")
    if src > 0 and dst > 0 and lines[src].strip():
        w = lines[:]
        moved = w[src]
        del w[src]
        dst2 = dst - 1 if dst > src else dst
        w.insert(dst2, moved)
        out.append(("move a line from §11.3 to §11.4", "PLACEMENT", "\n".join(w)))

    # 6. change a table cell.
    for i, l in enumerate(lines):
        if l.startswith("| L44 |"):
            w = lines[:]
            w[i] = l.replace("exceeds", "is greater than", 1)
            out.append(("reword register row L44", "CONTENT", "\n".join(w)))
            break

    return out


def selftest() -> int:
    print("self-test — historical commits, then mutations of the current document\n")
    bad = 0

    print("  historical (answers known from each commit's own ADR):")
    for rev, expect, why in CASES:
        before, after = git("show", f"{rev}^:{SPEC}"), git("show", f"{rev}:{SPEC}")
        if not before or not after:
            print(f"    SKIP {rev}  (not in this clone)")
            continue
        got = verdict(before, after)
        ok = got == expect
        bad += 0 if ok else 1
        print(f"    {'ok  ' if ok else 'FAIL'} {rev}  want {expect:9s} got {got:9s}  {why[:64]}")

    print()
    print("  regression — the identifier-keyed version missed these five sections")
    print("  of ADR-0102's commit because later citations overwrote the definition:")
    before, after = git("show", "830f08e^:" + SPEC), git("show", "830f08e:" + SPEC)
    if before and after:
        pb, pa = parse(before)[0], parse(after)[0]
        for sec in ("4.2", "11.2", "11.3", "20.3", "22.2"):
            hit = pb.get(sec, "") != pa.get(sec, "")
            bad += 0 if hit else 1
            print(f"    {'ok  ' if hit else 'FAIL'} §{sec} seen as changed")

    print()
    print("  synthetic (all three verdicts exercised against the current document):")
    spec = (REPO / SPEC).read_text(encoding="utf-8")
    cases = synthetic(spec)
    if len(cases) < 6:
        print(f"    FAIL only {len(cases)}/6 mutations could be built")
        bad += 1
    for name, expect, mutated in cases:
        got = verdict(spec, mutated)
        ok = got == expect
        bad += 0 if ok else 1
        print(f"    {'ok  ' if ok else 'FAIL'} want {expect:9s} got {got:9s}  {name}")

    print()
    print("self-test PASSED" if not bad else f"self-test FAILED — {bad} case(s)")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", metavar="REV", default="HEAD")
    ap.add_argument("--rev", metavar="COMMIT")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.rev:
        before = git("show", f"{args.rev}^:{SPEC}")
        after = git("show", f"{args.rev}:{SPEC}")
        label = f"commit {args.rev}"
    else:
        before = git("show", f"{args.base}:{SPEC}")
        after = (REPO / SPEC).read_text(encoding="utf-8")
        label = f"working tree against {args.base}"

    if not before or not after:
        print(f"could not read both revisions of {SPEC}")
        return 1

    print(f"editorial check — {label}")
    return compare(before, after, args.strict, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
