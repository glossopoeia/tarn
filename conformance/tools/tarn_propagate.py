#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""Propagation check: what else restates the rule you just changed.

Every byte-level defect this project has found since round 7 has been the same
shape. A rule is repaired in one place, and the places that restate it are left
standing at the old meaning:

  ADR-0067 made an unimplemented major unjudgeable in §2.3 and §21.6, and left
  §21.2's F1 registering it as a violation.
  ADR-0067 added the directory minimums to `[R-ERR-05]`, and left Appendix B
  claiming to collect every named constant.
  ADR-0071 broadened §4.7's `structural`, and left §13.1 calling fill semantic.
  ADR-0071 wrote a reject-tile bar into §20.3 step 2 that step 4 contradicts.

None of these needed a cleanroom round to find. Each is two passages sharing
the terms of one rule, changed in one and not the other — which a machine can
see. `tarn_check.py` checks the document against itself at rest; this checks a
*change* against the document.

    tarn_propagate.py                     # working tree against HEAD
    tarn_propagate.py --base <rev>        # against any revision
    tarn_propagate.py --rev <commit>      # what that commit should have swept
    tarn_propagate.py --threshold 3       # raise the bar for a flagged site

For each changed hunk it extracts the rule's *anchors* — the requirement ids
and register rows it cites, the field and structure names it uses, the terms it
emboldens, and its distinctive phrasing — then reports every other passage
carrying enough of the same anchors, and whether that passage was changed too.

Exit status is 1 when a site shares anchors with a change and was not itself
touched, unless the pair is acknowledged in `propagation-acks.txt` with a
reason. An acknowledged pair is a judgement on the record, which is the same
discipline `SKIPPED` and `COMPLETENESS_DISPOSITIONED` use elsewhere.
"""

from __future__ import annotations

import argparse
import collections
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "spec" / "tarn.md"
ACKS = Path(__file__).resolve().parent / "propagation-acks.txt"

# Anchors that name the same rule wherever they appear. Ordered strongest first;
# the weight is how much one shared anchor counts toward the threshold.
RULE_ID = re.compile(r"\[(R-[A-Z]{3}-\d{2})\]")
ROW_ID = re.compile(r"\b([FLTR]\d{1,2})\b")
IDENT = re.compile(r"`([a-z_][a-z0-9_]{3,})`")
BOLD = re.compile(r"\*\*([a-z][a-z \-]{2,30})\*\*")
WORD = re.compile(r"[a-z][a-z'\-]+")
ROW_DEF = re.compile(r"^\| [FLTR]\d{1,2} \|")

WEIGHT = {"rule": 3, "row": 3, "ident": 2, "bold": 2, "phrase": 1}

# A shingle this common is prose, not a rule's fingerprint; this rare and it is
# a hapax that links nothing. The band was chosen by measuring the document.
SHINGLE_MIN, SHINGLE_MAX = 2, 6


def sh(*args: str) -> str:
    return subprocess.run(args, capture_output=True, text=True, cwd=REPO).stdout


class Doc:
    """The specification, indexed by line, section and requirement span."""

    def __init__(self, text: str) -> None:
        self.lines = text.split("\n")
        self.section = self._sections()
        self.rule_at = self._rule_spans()
        self.shingles = self._shingle_index()

    def _sections(self) -> list[str]:
        out, cur = [], "(front matter)"
        for line in self.lines:
            m = re.match(r"^#{2,4}\s+(?:§)?((?:Appendix [A-H])|[\d.]+)", line)
            if m:
                cur = m.group(1)
            out.append(cur)
        return out

    def _rule_spans(self) -> list[str | None]:
        """Map each line to the requirement whose span it lies in.

        A requirement identifier closes the text it labels, so a span runs from
        just after the previous identifier to the line carrying its own.
        """
        out: list[str | None] = [None] * len(self.lines)
        start = 0
        for i, line in enumerate(self.lines):
            for rid in RULE_ID.findall(line):
                if f"`[{rid}]`" in line:
                    for j in range(start, i + 1):
                        if out[j] is None:
                            out[j] = rid
                    start = i + 1
                    break
        return out

    def _shingle_index(self) -> dict[tuple, list[int]]:
        idx: dict[tuple, list[int]] = collections.defaultdict(list)
        for i, line in enumerate(self.lines):
            w = WORD.findall(line.lower())
            for k in range(len(w) - 2):
                idx[tuple(w[k:k + 3])].append(i)
        return {k: v for k, v in idx.items() if SHINGLE_MIN <= len(set(v)) <= SHINGLE_MAX}

    def anchors(self, lo: int, hi: int) -> dict[str, set]:
        """Every anchor the lines [lo, hi) carry."""
        blob = "\n".join(self.lines[lo:hi])
        a = {
            "rule": set(RULE_ID.findall(blob)),
            "row": set(ROW_ID.findall(blob)),
            "ident": {i for i in IDENT.findall(blob) if self.rare(i)},
            "bold": {b.strip() for b in BOLD.findall(blob) if self.rare(b.strip())},
            "phrase": set(),
        }
        for k, lines in self.shingles.items():
            if any(lo <= n < hi for n in lines):
                a["phrase"].add(k)
        return a

    def rare(self, term: str) -> bool:
        """A term is an anchor only if it names something in particular.

        `slack` occurs on 40 lines and links nothing; `crc_of_crc_array` occurs
        on six and links exactly the passages about it. The ceiling is the same
        judgement the shingle band makes, applied to single terms.
        """
        pat = re.compile(r"\b" + re.escape(term) + r"\b", re.I)
        return 2 <= sum(1 for l in self.lines if pat.search(l)) <= 12

    def sites(self, kind: str, anchor) -> set[int]:
        """Every line carrying this anchor."""
        if kind == "phrase":
            return set(self.shingles.get(anchor, []))
        # Markup is not part of the term. A field named `fill` in one passage
        # and "the fill value" in another is the same anchor -- and that exact
        # pair is how §4.7's taxonomy and §13.1's gloss drifted apart under
        # ADR-0071 without any tool seeing it.
        pat = {
            "rule": lambda a: re.compile(r"\[" + re.escape(a) + r"\]"),
            "row": lambda a: re.compile(r"\b" + re.escape(a) + r"\b"),
            "ident": lambda a: re.compile(r"\b" + re.escape(a) + r"\b"),
            "bold": lambda a: re.compile(r"\b" + re.escape(a) + r"\b", re.I),
        }[kind](anchor)
        return {i for i, l in enumerate(self.lines) if pat.search(l)}


def changed_hunks(base: str, rev: str | None) -> list[tuple[int, int]]:
    """New-side line ranges the diff touches, 0-based, half-open."""
    if rev:
        diff = sh("git", "diff", "-U0", f"{rev}^", rev, "--", "spec/tarn.md")
    else:
        diff = sh("git", "diff", "-U0", base, "--", "spec/tarn.md")
    out = []
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff, re.M):
        start, count = int(m.group(1)), int(m.group(2) or 1)
        if count:
            out.append((start - 1, start - 1 + count))
    return out


def load_acks() -> set[tuple[str, str]]:
    acks = set()
    if ACKS.exists():
        for line in ACKS.read_text(encoding="utf-8").split("\n"):
            line = line.split("#", 1)[0].strip()
            if not line or "->" not in line:
                continue
            a, b = line.split("->", 1)
            acks.add((a.strip(), b.split(":", 1)[0].strip()))
    return acks


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", default="HEAD")
    ap.add_argument("--rev")
    ap.add_argument("--threshold", type=int, default=4,
                    help="minimum weighted anchor overlap to flag a site")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    text = sh("git", "show", f"{args.rev}:spec/tarn.md") if args.rev else SPEC.read_text(encoding="utf-8")
    doc = Doc(text)
    hunks = changed_hunks(args.base, args.rev)
    if not hunks:
        print("no change to spec/tarn.md — nothing to propagate")
        return 0

    touched = {i for lo, hi in hunks for i in range(lo, hi)}
    acks = load_acks()
    findings = []

    for lo, hi in hunks:
        anchors = doc.anchors(lo, hi)
        src_rule = next((doc.rule_at[i] for i in range(lo, hi) if doc.rule_at[i]), None)
        src_sec = doc.section[lo] if lo < len(doc.section) else "?"
        score: dict[int, list[str]] = collections.defaultdict(list)
        for kind, items in anchors.items():
            for a in items:
                for line in doc.sites(kind, a):
                    if lo <= line < hi:
                        continue
                    label = " ".join(a) if kind == "phrase" else a
                    score[line].append(f"{kind}:{label}")
        # Collapse adjacent lines into one site, keeping the best-scoring line.
        by_span: dict[tuple, tuple[int, list[str]]] = {}
        for line, hits in score.items():
            w = sum(WEIGHT[h.split(":", 1)[0]] for h in hits)
            if w < args.threshold:
                continue
            key = (doc.section[line], doc.rule_at[line])
            if key not in by_span or w > sum(WEIGHT[h.split(":", 1)[0]] for h in by_span[key][1]):
                by_span[key] = (line, hits)
        for (sec, rule), (line, hits) in by_span.items():
            if line in touched:
                continue                      # changed in the same diff: swept
            # Two register rows restating each other is not a propagation
            # failure -- §21.1 licenses the register to restate its rules, and
            # REG-01..08 own that relationship. Without this, one renumbering
            # buries every real finding under a table that is self-similar by
            # design: ADR-0067's sweep produced fourteen row-to-row pairs
            # above the two defects the next round actually found.
            if ROW_DEF.match(doc.lines[line]) and any(
                    ROW_DEF.match(doc.lines[i]) for i in range(lo, hi)):
                continue
            pair = (src_rule or f"§{src_sec}", rule or f"§{sec}")
            if pair in acks:
                continue
            findings.append({
                "src_sec": src_sec, "src_rule": src_rule, "src_lo": lo + 1,
                "sec": sec, "rule": rule, "line": line + 1,
                "hits": sorted(set(hits), key=lambda h: -WEIGHT[h.split(":", 1)[0]]),
                "weight": sum(WEIGHT[h.split(":", 1)[0]] for h in set(hits)),
                "text": doc.lines[line].strip()[:96],
            })

    findings.sort(key=lambda f: -f["weight"])
    print(f"propagation check — {len(hunks)} changed hunk(s) in spec/tarn.md\n")
    if not findings:
        print("  no unswept restatement found above the threshold")
        return 0

    for f in findings:
        src = f"§{f['src_sec']}" + (f" [{f['src_rule']}]" if f["src_rule"] else "")
        dst = f"§{f['sec']}" + (f" [{f['rule']}]" if f["rule"] else "")
        print(f"  {src} (line {f['src_lo']}) -> {dst} (line {f['line']}), weight {f['weight']}")
        print(f"      shared: {', '.join(f['hits'][:6])}")
        if not args.quiet:
            print(f"      there:  {f['text']}")
    print(f"\n{len(findings)} site(s) restate a rule this change touched and were not changed with it.")
    print("Change them, or record the judgement in conformance/tools/propagation-acks.txt")
    print("as  <source> -> <site>: <reason>")
    return 1


if __name__ == "__main__":
    sys.exit(main())
