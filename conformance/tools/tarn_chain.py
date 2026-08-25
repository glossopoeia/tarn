#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""Audit-chain check: has every repair to the spec been read by something?

ADR-0081 put a repair audit in front of every cleanroom round, because for four
consecutive rounds the defect the next round found was in the previous round's
repair. The audit works. What nothing tracked was whether it *ran* — and
ADR-0095's diff was skipped entirely, found weeks later only by walking the
chain by hand. ADR-0097 recorded the invariant behind it and observed that it is
mechanically checkable from git. This is that check.

    tarn_chain.py                    # the open interval: since the last charter
    tarn_chain.py --full             # every spec-touching commit in history
    tarn_chain.py --since <rev>      # from a chosen revision
    tarn_chain.py -v                 # name the covering artifact for each commit

THE INVARIANT, AND WHY IT IS NOT THE ONE ADR-0097 WROTE DOWN

ADR-0097 states it as "every commit touching spec/tarn.md between two charters
appears in some audit's range." Run literally, that reports two false positives:
ADR-0092 landed two minutes before round 24's charter and ADR-0097 one minute
before round 25's, and neither was audited. Neither is a gap. A repair committed
just before a charter is handed to the *round* rather than to an audit, and the
round is the stronger reading of the two — fresh context over the whole
document, not one auditor over a diff. Round 25's own charter says so in terms:
"the most recent repair of all is unaudited, because auditing every repair of
every repair does not converge and a fresh reading is what this round is for."

So the invariant is a disjunction:

    every commit touching spec/tarn.md is covered by some audit's range,
    OR it is followed by a charter, whose round read it.

Which collapses to something sharper and easier to act on: **the only commits
that can violate it are those after the most recent charter.** Those have no
round coming to read them, so an audit must. That open interval is what this
tool checks by default, and it is exactly the set the next charter closes.

WHAT COUNTS AS AN AUDIT'S RANGE

The committed `*.diff` artifacts under `docs/cleanroom/`. A commit is covered
when its payload — the added and removed lines, whitespace-normalised, hunk
headers and context discarded — is wholly contained in one artifact. Coverage
spread across two artifacts is reported as partial and does not satisfy the
invariant, because an auditor read neither commit whole.

Uncommitted artifacts on disk count too: the audit for the most recent repair
is normally still in the working tree when this runs, which is the moment the
answer matters most.

Exit status is 1 when a commit in the checked range is covered by nothing.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = "spec/tarn.md"
CLEANROOM = "docs/cleanroom"
CHARTER = re.compile(r"^Cleanroom round \d+: charter", re.I)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args], capture_output=True, text=True, check=False
    ).stdout


def payload(diff_text: str) -> frozenset[str]:
    """The lines a diff actually changes, normalised.

    Hunk headers carry line numbers that shift between a commit and an artifact
    written later, and context lines are shared by unrelated diffs. Neither can
    be compared. What is stable is the added and removed text itself.
    """
    out = set()
    for line in diff_text.split("\n"):
        if line.startswith(("+++", "---", "diff ", "index ", "@@", "old mode", "new mode")):
            continue
        if line[:1] in "+-" and line[1:].strip():
            out.add(line[0] + " ".join(line[1:].split()))
    return frozenset(out)


def artifacts() -> list[tuple[str, frozenset[str]]]:
    """Every audit diff under docs/cleanroom — committed or still in the tree."""
    found = []
    root = REPO / CLEANROOM
    if root.is_dir():
        for path in sorted(root.rglob("*.diff")):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            found.append((str(path.relative_to(REPO)), payload(text)))
    return found


def spec_commits(since: str | None) -> list[tuple[str, str]]:
    rng = [f"{since}..HEAD"] if since else []
    raw = git("log", "--reverse", "--format=%h%x00%s", *rng, "--", SPEC).strip()
    return [tuple(l.split("\x00", 1)) for l in raw.split("\n") if l]


def last_charter() -> tuple[str, str] | None:
    raw = git("log", "--format=%h%x00%s").strip()
    for line in raw.split("\n"):
        if not line:
            continue
        h, s = line.split("\x00", 1)
        if CHARTER.match(s):
            return h, s
    return None


def charters_after(commit: str) -> list[tuple[str, str]]:
    raw = git("log", "--reverse", "--format=%h%x00%s", f"{commit}..HEAD").strip()
    out = []
    for line in raw.split("\n"):
        if not line:
            continue
        h, s = line.split("\x00", 1)
        if CHARTER.match(s):
            out.append((h, s))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--since", metavar="REV", help="check from this revision forward")
    ap.add_argument("--full", action="store_true", help="check all of history")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    charter = last_charter()
    if args.full:
        since, scope = None, "all history"
    elif args.since:
        since, scope = args.since, f"since {args.since}"
    elif charter:
        since = charter[0]
        scope = f"since the last charter ({charter[0]} {charter[1]})"
    else:
        since, scope = None, "all history (no charter found)"

    arts = artifacts()
    commits = spec_commits(since)

    print(f"audit chain — {scope}")
    print(f"  {len(commits)} commit(s) touching {SPEC}; {len(arts)} audit artifact(s) on disk")
    print()

    open_gaps = []
    for h, subject in commits:
        want = payload(git("show", h, "--", SPEC))
        if not want:
            continue
        covering = [name for name, have in arts if want <= have]
        following = charters_after(h)
        if covering:
            verdict, how = "ok", f"audited — {covering[0]}"
        elif following:
            verdict, how = "ok", f"read by round — {following[0][1]}"
        else:
            best, frac = None, 0.0
            for name, have in arts:
                f = len(want & have) / len(want)
                if f > frac:
                    best, frac = name, f
            union = set().union(*(have for _, have in arts)) if arts else set()
            spread = len(want & union) / len(want)
            verdict = "GAP"
            how = "covered by nothing"
            if frac:
                how = f"best artifact {best} covers {frac:.0%}; union {spread:.0%} — partial is not coverage"
            open_gaps.append((h, subject, how))

        if args.verbose or verdict == "GAP":
            mark = "  " if verdict == "ok" else "! "
            print(f"{mark}{h} {subject[:58]:58s} {how}")

    print()
    if open_gaps:
        print(f"FAIL — {len(open_gaps)} commit(s) in the open interval are unaudited:")
        for h, subject, how in open_gaps:
            print(f"  {h} {subject}")
            print(f"      {how}")
        print()
        print("  These have no round coming to read them. Audit them before the next")
        print("  charter, or the next round reads a repair nothing has checked.")
        return 1

    print(f"PASS — every commit in range is audited or was read by a following round.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
