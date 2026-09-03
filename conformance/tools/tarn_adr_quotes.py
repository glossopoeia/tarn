#!/usr/bin/env python3
"""Check that what an ADR quotes from the spec is still in the spec.

THE GAP THIS CLOSES. Three times in one cycle an ADR described the text it
authorised and the description was wrong, and nothing caught it:

  * ADR-0113 said "Neither bar is witnessed" after ADR-0114 withdrew one of the
    two, and grounded unwitnessedness on a claim `[R-LIF-06]` and `[R-PRV-03]`
    deny in terms.
  * ADR-0115's Decision stated the §21.7 test over the wrong subject, with the
    wrong instrument, and with the quantifier mismatch its own audit had found
    and the spec had already repaired.
  * ADR-0117 said "a new item pins ..." where the clause had been added to an
    existing item, and misquoted a quantifier in a decision *about* quantifiers.

Every cleanroom agent reads `spec/tarn.md` and nothing else, so no round can see
this. `tarn_propagate` compares spec passages to spec passages. `tarn_editorial`
compares spec revisions. **Nothing compared an ADR's prose to the text it
authorises**, which is exactly what ADR-0076 recorded as a place a rule can hide.

WHAT IT CHECKS, AND WHAT IT DOES NOT. This is a quotation checker, not a
semantic one. It finds every span an ADR marks as verbatim — the project's
convention is `*"..."*` — normalises markup and whitespace (and the `> ` a
blockquote wrap inserts), and reports the spans that are no longer in
`spec/tarn.md`. It cannot see a paraphrase that has drifted, only a quotation
that has. Coverage today is the 21 ADRs using the convention; an ADR that
paraphrases throughout is invisible to it, and that limit is the reason a
hand-check of a decision against what landed is still owed.

AN ABSENT QUOTE IS NOT AUTOMATICALLY A DEFECT. An ADR often quotes the text it
is *replacing*, which is absent by design and correctly so. Those are recorded
in `adr-quote-acks.txt`, one line per quote, with the reason. An unacknowledged
absence is what this reports.

    python3 tarn_adr_quotes.py                 # the ADRs this tree changes -- gates
    python3 tarn_adr_quotes.py --all           # the whole trail -- reports only
    python3 tarn_adr_quotes.py 0117            # one, by number or path
    python3 tarn_adr_quotes.py --selftest

Run it before committing an ADR, beside `tarn_check`.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = os.path.join(ROOT, "spec", "tarn.md")
ADRS = os.path.join(ROOT, "docs", "decisions")
ACKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adr-quote-acks.txt")

QUOTE = re.compile(r'\*"(.+?)"\*', re.S)


def normalise(text: str) -> str:
    """Markup- and wrap-insensitive form.

    The document is hard-wrapped and a blockquote wrap inserts "> ", so a
    literal comparison fails on text that is present. Bold and code markers are
    stripped because an ADR routinely bolds a word inside a quotation for
    emphasis the source does not carry.
    """
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    text = text.replace("**", "").replace("`", "").replace("*", "")
    return " ".join(text.split())


def load_acks() -> dict[tuple[str, str], str]:
    """(adr, quote-prefix) -> reason. A prefix matches any quote starting with it."""
    out: dict[tuple[str, str], str] = {}
    if not os.path.exists(ACKS):
        return out
    for line in open(ACKS, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        head, _, reason = line.partition(":")
        adr, _, prefix = head.partition("|")
        out[(adr.strip(), prefix.strip())] = reason.strip()
    return out


def check_adr(path: str, spec_norm: str, acks) -> tuple[int, list[str], list[str]]:
    src = open(path, encoding="utf-8").read()
    name = os.path.basename(path).split("-")[0]
    quotes = QUOTE.findall(src)
    absent, unacked = [], []
    for q in quotes:
        n = normalise(q)
        if not n or n in spec_norm:
            continue
        absent.append(n)
        if not any(a == name and n.startswith(p) for (a, p) in acks):
            unacked.append(n)
    return len(quotes), absent, unacked


def main(argv) -> int:
    if "--selftest" in argv:
        return selftest()
    spec_norm = normalise(open(SPEC, encoding="utf-8").read())
    acks = load_acks()

    picks = [a for a in argv[1:] if not a.startswith("-")]
    every = "--all" in argv

    def all_adrs():
        return [os.path.join(ADRS, p) for p in sorted(os.listdir(ADRS))
                if re.match(r"^\d{4}-.*\.md$", p)]

    if picks:
        targets = [p for p in all_adrs()
                   if any(os.path.basename(p).startswith(k.zfill(4)) or k in p
                          for k in picks)]
        scope = "named"
    elif every:
        targets = all_adrs()
        scope = "the whole trail"
    else:
        # DEFAULT: only the ADRs this working tree changes. An ADR that
        # described the spec correctly when it was written and no longer does is
        # a historical record, not a defect -- the spec is meant to move. The
        # drift worth gating on is an ADR describing text AS IT LANDS, which is
        # what the three failures in the docstring were. Gating on 46 historical
        # absences would make this a guard whose output is always the same, and
        # a guard nobody reads is worse than none.
        import subprocess
        r = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", "docs/decisions"],
                           capture_output=True, text=True, cwd=ROOT)
        u = subprocess.run(["git", "ls-files", "--others", "--exclude-standard",
                            "docs/decisions"], capture_output=True, text=True, cwd=ROOT)
        names = [n for n in (r.stdout + u.stdout).split("\n") if n.strip()]
        targets = [os.path.join(ROOT, n) for n in names
                   if re.match(r"^\d{4}-.*\.md$", os.path.basename(n))]
        scope = "ADRs this working tree changes"
        if not targets:
            print("no ADR changed in the working tree; nothing to check")
            print("(--all sweeps the trail, and reports rather than gates)")
            return 0
    print(f"checking {scope}\n")

    total_q = total_absent = 0
    failing = []
    for path in targets:
        nq, absent, unacked = check_adr(path, spec_norm, acks)
        total_q += nq
        total_absent += len(absent)
        if not nq:
            continue
        mark = "FAIL" if unacked else "ok  "
        print(f"  {mark} {os.path.basename(path)[:58]:58} {nq - len(absent)}/{nq} verbatim")
        for u in unacked:
            print(f"         ✗ not in spec/tarn.md, and not acknowledged:")
            print(f"           {u[:150]}")
        if unacked:
            failing.append(os.path.basename(path))

    print()
    print(f"{total_q} quoted span(s) across {len(targets)} ADR(s); {total_absent} absent")
    if failing and every:
        print(f"\n{len(failing)} ADR(s) quote text the spec no longer carries. Over the whole "
              f"trail this is expected: an ADR records the text as it stood. Reported, not failed.")
        return 0
    if failing:
        print(f"\nFAIL — {len(failing)} ADR(s) quote text the spec no longer carries, "
              f"unacknowledged: {', '.join(failing)}")
        print("Either the ADR is describing text that moved under it — the defect this "
              "exists to find — or the quote is of superseded text on purpose, in which "
              "case record it in adr-quote-acks.txt as  <adr>|<quote prefix>: <reason>")
        return 1
    print("\nPASS — every quoted span is in the spec or acknowledged as superseded")
    return 0


def selftest() -> int:
    ok = True

    def check(cond, label):
        nonlocal ok
        print("  %-58s %s" % (label, "ok" if cond else "FAIL"))
        ok = ok and cond

    # The wrap forms the checker exists to see through.
    check(normalise("a phrase\nthat wraps") == "a phrase that wraps",
          "hard wrap normalised")
    check(normalise("> a phrase\n> in a blockquote") == "a phrase in a blockquote",
          "blockquote wrap normalised (the '> ' a wrap inserts)")
    check(normalise("**bold** and `code`") == "bold and code",
          "bold and code markers stripped")
    # An ADR quoting text that is present must pass, and one quoting text that
    # is absent must fail -- built as a pair so neither verdict is the only one
    # this can give.
    spec = normalise("The register carries a row for every condition.")
    present = normalise("carries a row for every condition")
    absent = normalise("carries a row exactly where it is detectable")
    check(present in spec, "a quote that IS present is found")
    check(absent not in spec, "a quote that is NOT present is reported")
    # The ack matcher is a prefix match on the normalised quote.
    acks = {("0117", "carries a row exactly where"): "quotes the superseded sentence"}
    check(any(a == "0117" and absent.startswith(p) for (a, p) in acks),
          "an acknowledged absence is matched by prefix")
    check(not any(a == "0115" and absent.startswith(p) for (a, p) in acks),
          "an ack for one ADR does not cover another")
    print("\nSELFTEST " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
