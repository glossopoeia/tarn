#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""The equivalence contract between two editions of spec/tarn.md (ADR-0133).

A readable edition may reorder, reword and cut explanatory prose. It may not
change what the document decides. This tool states, mechanically, the part of
"does not change the contents" that a script can see, and reports the rest for
a human or a fidelity round to judge:

    tarn_inventory.py <edition-a.md> <edition-b.md> [--reworded FILE] [--json OUT]
    tarn_inventory.py --selftest

HARD items (exit status 1 when any fails):
  * the requirement-ID inventory is identical (no ID missing, none added);
  * every ID's governing text is verbatim, or the ID is listed in --reworded
    with a justification (one line per ID: "R-CNT-08: why");
  * the error register (§21.2–§21.5) is row for row identical, keyed by label;
  * every defined term of §3.1 is still defined.
SOFT items (reported, never fatal): table rows and fenced blocks present in
one edition only; numbers inside labelled Example blocks; BCP 14 keyword
counts; headings in order; the count of labelled Note/Example/Rationale
blocks; a defined term whose definition text changed.

Scope, per ADR-0050's rule for these tools: it reads two files and reports.
It never edits either.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ID_RE = re.compile(r"`\[(R-[A-Z]+-\d+)\]`")
LABEL_RE = re.compile(r"^\|\s*([FLTR]\d+)\s*\|")
TERM_RE = re.compile(r"^- \*\*([^*]+)\*\*\s+—")
HEADING_RE = re.compile(r"^(#{2,6})\s+(.*?)\s*$")
FENCE_RE = re.compile(r"^```")
LIST_RE = re.compile(r"^(- |\* |\d+\. )")
NUMBER_RE = re.compile(r"0x[0-9A-Fa-f]+|\b\d[\d,]*(?:\.\d+)?\b")
KEYWORDS = ["MUST NOT", "MUST", "SHOULD NOT", "SHOULD", "MAY", "REQUIRED", "RECOMMENDED", "OPTIONAL"]


def norm(s: str) -> str:
    return " ".join(s.split())


def strip_quote(line: str) -> str:
    return re.sub(r"^>\s?", "", line)


def blocks(text: str) -> list[dict]:
    """Split a document into blocks: paragraphs, list items, table rows, fenced
    code, headings. Blockquote markers are stripped; a block records whether it
    sat in a labelled Note/Example/Rationale block and which section it is in."""
    out: list[dict] = []
    cur: list[str] = []
    section = "front matter"
    in_fence = False
    fence: list[str] = []
    label = None  # the label of the enclosing blockquote, if any

    def flush():
        nonlocal cur
        if cur:
            out.append({"kind": "para", "text": norm(" ".join(cur)), "section": section, "label": label})
            cur = []

    for raw in text.split("\n"):
        q = raw.startswith(">")
        line = strip_quote(raw)
        if in_fence:
            fence.append(line)
            if FENCE_RE.match(line.strip()):
                out.append({"kind": "fence", "text": "\n".join(fence[1:-1]).rstrip(), "section": section, "label": label})
                fence = []
                in_fence = False
            continue
        if FENCE_RE.match(line.strip()):
            flush()
            in_fence = True
            fence = [line]
            continue
        m = HEADING_RE.match(line)
        if m:
            flush()
            section = m.group(2)
            out.append({"kind": "heading", "text": line.strip(), "section": section, "label": None})
            label = None
            continue
        if not line.strip():
            flush()
            if not q:
                label = None  # an unquoted blank line ends the labelled block, after its last paragraph is flushed
            continue
        if not q and label is not None:
            flush()
            label = None
        lm = re.match(r"^\*\*(Note|Example|Rationale)\b", line.strip())
        if q and lm and not cur:
            label = lm.group(1)
        if line.lstrip().startswith("|"):
            flush()
            if re.match(r"^\|\s*-{2,}", line.strip()):
                continue  # separator row
            out.append({"kind": "row", "text": norm(line), "section": section, "label": label})
            continue
        if LIST_RE.match(line) and cur:
            flush()
        cur.append(line)
    flush()
    return out


def id_texts(bl: list[dict]) -> dict[str, str]:
    """Each requirement ID's governing text: the block the ID closes. An ID that
    closes no block (only cited) maps to the first block that contains it."""
    defining: dict[str, str] = {}
    cited: dict[str, str] = {}
    for b in bl:
        if b["kind"] not in ("para", "row"):
            continue
        t = b["text"]
        ids = ID_RE.findall(t)
        if not ids:
            continue
        tail = re.sub(r"[\s|]+$", "", t)
        m = ID_RE.search(tail[-24:])
        if m and tail.endswith("`[%s]`" % m.group(1)):
            defining.setdefault(m.group(1), t)
        for i in ids:
            cited.setdefault(i, t)
    for i, t in cited.items():
        defining.setdefault(i, t)
    return defining


def register_rows(text: str) -> dict[str, str]:
    lines = text.split("\n")
    rows: dict[str, str] = {}
    active = False
    for line in lines:
        m = HEADING_RE.match(strip_quote(line))
        if m:
            h = m.group(2)
            active = bool(re.match(r"21\.[2-5]\b", h))
            continue
        if active:
            lm = LABEL_RE.match(strip_quote(line).strip())
            if lm:
                rows[lm.group(1)] = norm(strip_quote(line))
    return rows


def terms(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    active = False
    cur_term = None
    cur: list[str] = []
    for raw in text.split("\n"):
        line = strip_quote(raw)
        m = HEADING_RE.match(line)
        if m:
            if active and cur_term:
                out[cur_term] = norm(" ".join(cur))
            active = m.group(2).startswith("3.1")
            cur_term, cur = None, []
            continue
        if not active:
            continue
        tm = TERM_RE.match(line)
        if tm:
            if cur_term:
                out[cur_term] = norm(" ".join(cur))
            cur_term, cur = tm.group(1).strip(), [line]
        elif cur_term and line.strip():
            cur.append(line)
    if active and cur_term:
        out[cur_term] = norm(" ".join(cur))
    return out


def example_numbers(bl: list[dict]) -> Counter:
    c: Counter = Counter()
    for b in bl:
        if b["label"] == "Example" and b["kind"] in ("para", "row", "fence"):
            c.update(NUMBER_RE.findall(b["text"]))
    return c


def keyword_counts(text: str) -> dict[str, int]:
    body = norm(" ".join(strip_quote(l) for l in text.split("\n")))
    out = {}
    for k in KEYWORDS:
        n = len(re.findall(r"\b%s\b" % k, body))
        out[k] = n
    out["MUST"] -= out["MUST NOT"]
    out["SHOULD"] -= out["SHOULD NOT"]
    return out


def read_reworded(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    out = {}
    for line in Path(path).read_text(encoding="utf-8").split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            sys.exit("reworded list: each line is 'R-XXX-NN: reason' — got %r" % line)
        rid, why = line.split(":", 1)
        out[rid.strip()] = why.strip()
    return out


def compare(a_text: str, b_text: str, reworded: dict[str, str]) -> dict:
    A, B = blocks(a_text), blocks(b_text)
    rep: dict = {"hard": [], "soft": [], "info": {}}

    # IDs
    ia, ib = id_texts(A), id_texts(B)
    missing = sorted(set(ia) - set(ib))
    added = sorted(set(ib) - set(ia))
    for i in missing:
        rep["hard"].append(("ID_MISSING", i, "in A, not in B"))
    for i in added:
        rep["hard"].append(("ID_ADDED", i, "in B, not in A"))
    changed = []
    for i in sorted(set(ia) & set(ib)):
        if ia[i] != ib[i]:
            d = "\n".join(difflib.unified_diff(ia[i].split(" "), ib[i].split(" "), lineterm="", n=2))
            if i in reworded:
                rep["soft"].append(("ID_REWORDED_LISTED", i, reworded[i]))
            else:
                rep["hard"].append(("ID_TEXT_CHANGED", i, d))
            changed.append(i)
    rep["info"]["ids"] = {"a": len(ia), "b": len(ib), "changed": changed}
    for i in sorted(reworded):
        if i not in changed and i in ia:
            rep["soft"].append(("REWORDED_LIST_STALE", i, "listed as reworded but verbatim in B"))

    # register
    ra, rb = register_rows(a_text), register_rows(b_text)
    for lab in sorted(set(ra) - set(rb)):
        rep["hard"].append(("REGISTER_ROW_MISSING", lab, ra[lab][:120]))
    for lab in sorted(set(rb) - set(ra)):
        rep["hard"].append(("REGISTER_ROW_ADDED", lab, rb[lab][:120]))
    for lab in sorted(set(ra) & set(rb)):
        if ra[lab] != rb[lab]:
            d = "\n".join(difflib.unified_diff(ra[lab].split(" | "), rb[lab].split(" | "), lineterm="", n=0))
            rep["hard"].append(("REGISTER_ROW_CHANGED", lab, d))
    rep["info"]["register_rows"] = {"a": len(ra), "b": len(rb)}

    # terms
    ta, tb = terms(a_text), terms(b_text)
    for t in sorted(set(ta) - set(tb)):
        rep["hard"].append(("TERM_MISSING", t, "defined in A's §3.1, not in B's"))
    for t in sorted(set(tb) - set(ta)):
        rep["soft"].append(("TERM_ADDED", t, "defined in B's §3.1, not in A's"))
    for t in sorted(set(ta) & set(tb)):
        if ta[t] != tb[t]:
            rep["soft"].append(("TERM_TEXT_CHANGED", t, "definition reworded; read both"))
    rep["info"]["terms"] = {"a": len(ta), "b": len(tb)}

    # tables and fences as multisets
    for kind, name in (("row", "TABLE_ROW"), ("fence", "FENCE")):
        reg = lambda b: b["kind"] == "row" and LABEL_RE.match(b["text"])
        ca = Counter(b["text"] for b in A if b["kind"] == kind and not reg(b))
        cb = Counter(b["text"] for b in B if b["kind"] == kind and not reg(b))
        for t, n in sorted((ca - cb).items()):
            rep["soft"].append((name + "_ONLY_IN_A", str(n), t[:140]))
        for t, n in sorted((cb - ca).items()):
            rep["soft"].append((name + "_ONLY_IN_B", str(n), t[:140]))

    # example numbers
    na, nb = example_numbers(A), example_numbers(B)
    only_a, only_b = na - nb, nb - na
    if only_a or only_b:
        rep["soft"].append(("EXAMPLE_NUMBERS", "in A only: %s; in B only: %s" % (dict(only_a), dict(only_b)),
                            "a worked example's figure changed, or an example moved out of a labelled block"))

    # keywords
    ka, kb = keyword_counts(a_text), keyword_counts(b_text)
    for k in KEYWORDS:
        if ka[k] != kb[k]:
            rep["soft"].append(("KEYWORD_COUNT", k, "A %d, B %d" % (ka[k], kb[k])))
    rep["info"]["keywords"] = {"a": ka, "b": kb}

    # headings and labelled blocks
    ha = [b["text"] for b in A if b["kind"] == "heading"]
    hb = [b["text"] for b in B if b["kind"] == "heading"]
    if ha != hb:
        d = [l for l in difflib.unified_diff(ha, hb, lineterm="", n=0) if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
        rep["soft"].append(("HEADINGS", "%d in A, %d in B" % (len(ha), len(hb)), "\n".join(d[:40])))
    la = Counter(b["label"] for b in A if b["label"] and b["kind"] == "para")
    lb = Counter(b["label"] for b in B if b["label"] and b["kind"] == "para")
    rep["info"]["labelled_paragraphs"] = {"a": dict(la), "b": dict(lb)}
    return rep


def render(rep: dict, a: str, b: str) -> str:
    out = ["inventory — %s against %s" % (a, b), ""]
    info = rep["info"]
    out.append("  IDs %d/%d (%d reworded); register rows %d/%d; terms %d/%d" % (
        info["ids"]["a"], info["ids"]["b"], len(info["ids"]["changed"]),
        info["register_rows"]["a"], info["register_rows"]["b"], info["terms"]["a"], info["terms"]["b"]))
    out.append("  keywords A: %s" % info["keywords"]["a"])
    out.append("  keywords B: %s" % info["keywords"]["b"])
    out.append("  labelled paragraphs A: %s  B: %s" % (info["labelled_paragraphs"]["a"], info["labelled_paragraphs"]["b"]))
    out.append("")
    if rep["hard"]:
        out.append("HARD (%d) — the contract is broken:" % len(rep["hard"]))
        for k, what, detail in rep["hard"]:
            out.append("  ✗ %-22s %s" % (k, what))
            for l in str(detail).split("\n")[:12]:
                out.append("        " + l)
    else:
        out.append("HARD: none — IDs, register and terms hold.")
    out.append("")
    if rep["soft"]:
        out.append("SOFT (%d) — reported for the reader or the fidelity round:" % len(rep["soft"]))
        for k, what, detail in rep["soft"]:
            out.append("  · %-22s %s" % (k, what))
            for l in str(detail).split("\n")[:6]:
                out.append("        " + l)
    else:
        out.append("SOFT: none.")
    out.append("")
    out.append("FAIL — %d hard item(s)" % len(rep["hard"]) if rep["hard"] else "PASS — the mechanical contract holds; what a script cannot see is the fidelity round's")
    return "\n".join(out)


def repo_spec() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "spec" / "tarn.md").exists():
            return p / "spec" / "tarn.md"
    sys.exit("could not locate spec/tarn.md above this file")


def selftest() -> int:
    a = repo_spec().read_text(encoding="utf-8")
    ok = True

    def check(cond, label):
        nonlocal ok
        print("  %-64s %s" % (label, "ok" if cond else "FAIL"))
        ok = ok and cond

    same = compare(a, a, {})
    check(not same["hard"] and not same["soft"], "an edition against itself: no hard item, no soft item")

    def edit(text, old, new, count=1):
        assert text.count(old) == count, (text.count(old), old[:60])
        return text.replace(old, new)

    b = edit(a, "MUST\nNOT clear them, and MUST NOT set any other", "MUST NOT set any other")
    r = compare(a, b, {})
    check(any(k == "ID_TEXT_CHANGED" and w == "R-CNT-08" for k, w, _ in r["hard"]), "a reworded ID paragraph is a hard item ([R-CNT-08])")
    check(any(k == "KEYWORD_COUNT" and w == "MUST NOT" for k, w, _ in r["soft"]), "  and the dropped MUST NOT shows in the keyword counts")
    r2 = compare(a, b, {"R-CNT-08": "selftest"})
    check(not r2["hard"] and any(k == "ID_REWORDED_LISTED" for k, _, _ in r2["soft"]), "  listed in --reworded, it is soft")

    b = edit(a, "`[R-CNT-03]`", "", a.count("`[R-CNT-03]`"))
    r = compare(a, b, {})
    check(any(k == "ID_MISSING" and w == "R-CNT-03" for k, w, _ in r["hard"]), "a removed ID is a hard item")

    b = edit(a, "| flags bits 0-15 |", "| flags bits 0-7 |")
    r = compare(a, b, {})
    check(any(k == "REGISTER_ROW_CHANGED" and w == "F19" for k, w, _ in r["hard"]), "a changed register instance is a hard item (F19)")

    b = edit(a, "- **file** —", "- **document** —")
    r = compare(a, b, {})
    check(any(k == "TERM_MISSING" and w == "file" for k, w, _ in r["hard"]), "a renamed §3.1 term is a hard item")

    b = edit(a, "32 · 20 + 4 = 644", "32 · 20 + 4 = 664")
    r = compare(a, b, {})
    check(any(k == "EXAMPLE_NUMBERS" for k, _, _ in r["soft"]), "a changed number in an Example is a soft item")

    b = edit(a, "#### 6.2 Trailer", "#### 6.2 The trailer")
    r = compare(a, b, {})
    check(any(k == "HEADINGS" for k, _, _ in r["soft"]) and not r["hard"], "a renamed heading is soft")

    # a paragraph that is not ID-carrying, cut: invisible to this tool, by design
    b = edit(a, "whatever their PE bits. One sub-record blocks the drop, a sub-record\nof a type the updater does not implement with MU = 1, the drop being\na modification of the scope it governs (the table's first row). A\ncommit never removes",
             "whatever their PE bits. A\ncommit never removes")
    r = compare(a, b, {})
    check(not r["hard"] and not any(k.startswith("ID") for k, _, _ in r["soft"]),
          "a cut sentence in a non-ID paragraph is invisible here (the fidelity round's job)")

    print("\nSELFTEST %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("a", nargs="?")
    ap.add_argument("b", nargs="?")
    ap.add_argument("--reworded")
    ap.add_argument("--json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.a and args.b):
        ap.error("two editions, or --selftest")
    a = Path(args.a).read_text(encoding="utf-8")
    b = Path(args.b).read_text(encoding="utf-8")
    rep = compare(a, b, read_reworded(args.reworded))
    print(render(rep, args.a, args.b))
    if args.json:
        Path(args.json).write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    return 1 if rep["hard"] else 0


if __name__ == "__main__":
    sys.exit(main())
