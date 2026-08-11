#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""Mechanical consistency checks for the TARN specification.

This specification restates its rules deliberately — in the error register, in
the appendices, in the conformance checklists, in section prose. That
redundancy is what makes it readable, and it is also where every defect found
in cleanroom rounds 4 and 5 lived: a rule changed in one place and left
standing in another. The checks here are the ones a machine can make.

Scope, per ADR-0050: this tool reads `spec/tarn.md` and reports. It never
writes to it, and it implements no part of the format — no reader, no decoder.
The one place it constructs bytes is Appendix A's minimal file, which it
rebuilds from the rules the specification states in order to compare against
the hex dump the specification prints.

Usage:
    tarn_check.py                 # every check
    tarn_check.py register        # the §21 error register only
    tarn_check.py spec            # spec-wide consistency only
    tarn_check.py coverage        # G5: the corpus against the register
    tarn_check.py --rev <commit>  # check a historical revision

Exit status is 0 when no check fails, 1 otherwise. Warnings never fail the
run: they mark places where the check is a heuristic and a human decides.
"""

from __future__ import annotations

import argparse
import re
import struct
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# --------------------------------------------------------------------------
# Facts this tool is allowed to know, each with the authority that fixes it.
# Everything else is derived from the document under test.
# --------------------------------------------------------------------------

# §2.2 permanently retires a withdrawn identifier and never reassigns it.
WITHDRAWN_IDS = {"R-SER-04": "§14.4 records the withdrawal"}

# ADR-0048 replaced both with "slack". A term that is retired in one place and
# alive in another is the exact defect class this tool exists to catch.
RETIRED_TERMS = {
    "dead space": "ADR-0048 — replaced by 'slack'",
    "declared padding": "ADR-0048 — replaced by 'slack'",
}

# REG-08 reads prose, so it has a residual set: rules that use the register's
# outcome vocabulary without naming a malformed file. Each is dispositioned here
# with its reason, so the check reports only what is *new*. A rule that stops
# belonging on this list should be removed from it, not silenced.
COMPLETENESS_DISPOSITIONED = {
    "R-CNF-07": "defines the outcome vocabulary; names no condition",
    "R-CNF-08": "defines the owning-scope mapping; names no condition",
    "R-ENC-05": "binds reader conduct — no I/O on an unverified integer; no file exhibits it",
    "R-ENC-07": "fixed-size structures; each row relying on it names its own structure",
    "R-ERR-04": "binds how a refusal is reported, not what a file may contain",
    "R-EXT-03": "routes experimental values to outcomes other rules assign; those rules carry the rows",
    "R-GEO-03": "grid arithmetic; the layer-scope overflow row is its row and cites it",
    "R-MTA-02": "binds reader conduct — metadata is never structural; no file exhibits it",
    "R-VEC-04": "constrains how the corpus is built, not what a file may contain",
    "R-LIF-08": "the verifier's coverage procedure; the violations it finds are the overlap rows'",
    "R-SLB-04": "a writer obligation whose detection it delegates to [R-SLB-03]; ADR-0057 deleted its row",
}

# AGENTS.md rule 5: BCP 14 keywords appear in ALL CAPS only. The verb forms
# are the ones a reader can misread as normative; the adjective forms are
# ordinary English often enough ("not optional", "a required field") that they
# are reported as warnings rather than failures.
BCP14_VERBS = r"\b(must not|must|shall not|shall|should not|should|may)\b"
BCP14_ADJECTIVES = r"\b(required|recommended|optional)\b"

# §21.1 fixes these vocabularies.
VALID_DETECTORS = {"reader", "verifier"}
VALID_DETECTION_POINTS = {
    "open", "layer access", "tile use", "extent use", "certification",
}

REGISTER_SECTIONS = [
    ("F", "#### 21.2", "file"),
    ("L", "#### 21.3", "layer"),
    ("T", "#### 21.4", "tile"),
    ("R", "#### 21.5", "ignored-record"),
]

ROW_RE = re.compile(
    r"^\| ([FLTR]\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$"
)
ID_RE = re.compile(r"R-[A-Z]{3}-\d{2}")
BACKTICKED_ID_RE = re.compile(r"`\[(R-[A-Z]{3}-\d{2})\]`")


class Report:
    """Collected findings. A failure fails the run; a warning does not."""

    def __init__(self) -> None:
        self.checks: list[tuple[str, str, list[str], str]] = []

    def add(self, cid: str, title: str, failures: list[str],
            warnings: list[str] | None = None) -> None:
        self.checks.append((cid, title, failures, warnings or []))

    @property
    def failed(self) -> bool:
        return any(f for _, _, f, _ in self.checks)

    def render(self) -> int:
        width = max(len(t) for _, t, _, _ in self.checks) + 2
        for cid, title, failures, warnings in self.checks:
            if failures:
                status = f"FAIL ({len(failures)})"
            elif warnings:
                status = f"warn ({len(warnings)})"
            else:
                status = "ok"
            print(f"  {cid}  {title.ljust(width, '.')} {status}")
            for line in failures:
                print(f"        ✗ {line}")
            for line in warnings:
                print(f"        · {line}")
        n_fail = sum(len(f) for _, _, f, _ in self.checks)
        n_warn = sum(len(w) for _, _, _, w in self.checks)
        print()
        if n_fail:
            print(f"FAILED — {n_fail} finding(s), {n_warn} warning(s)")
        else:
            print(f"PASS — 0 findings, {n_warn} warning(s)")
        return 1 if n_fail else 0


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------

class Spec:
    def __init__(self, text: str) -> None:
        self.text = text
        self.lines = text.split("\n")
        self.paragraphs = re.split(r"\n\s*\n", text)
        self.ids = sorted(set(ID_RE.findall(text)))
        self.rows = self._parse_register()

    def _section_lines(self, heading: str) -> list[str]:
        try:
            i = next(k for k, l in enumerate(self.lines) if l.startswith(heading))
        except StopIteration:
            return []
        j = next(
            (k for k in range(i + 1, len(self.lines))
             if self.lines[k].startswith("#### ")),
            len(self.lines),
        )
        return self.lines[i:j]

    def _parse_register(self) -> dict[str, list[dict]]:
        out: dict[str, list[dict]] = {}
        for prefix, heading, _scope in REGISTER_SECTIONS:
            rows = []
            for line in self._section_lines(heading):
                m = ROW_RE.match(line)
                if m:
                    rows.append({
                        "id": m.group(1), "condition": m.group(2),
                        "instances": m.group(3), "detector": m.group(4),
                        "detected": m.group(5), "rule": m.group(6),
                    })
            out[prefix] = rows
        return out

    @staticmethod
    def instance_count(cell: str) -> int:
        """§21.1: instances are semicolon-separated; a cell reading — is one."""
        if cell.strip() == "—":
            return 1
        return len([p for p in cell.split(";") if p.strip()])

    def definition_sites(self) -> dict[str, int]:
        """Where each requirement identifier is *defined*.

        The document's convention places the identifier after the requirement's
        final sentence, so a definition site is an occurrence preceded by a
        sentence terminator and followed by the end of its block, a new
        sentence, or the next list item. Every other occurrence — inside a
        parenthetical, or as a sentence's subject — is a reference.
        """
        sites: dict[str, int] = defaultdict(int)
        for para in self.paragraphs:
            flat = re.sub(r"\s+", " ", para).strip()
            if flat.startswith("|"):
                continue
            for m in BACKTICKED_ID_RE.finditer(flat):
                before = flat[:m.start()].rstrip()
                after = flat[m.end():]
                starts_block = before == "" or before.endswith((".", ":", "—"))
                ends_unit = (
                    after.strip() == ""
                    or re.match(r"\s+[A-Z“\"]", after)
                    or re.match(r"\s*[-*]\s", after)
                )
                if starts_block and ends_unit:
                    sites[m.group(1)] += 1
        return dict(sites)

    def defining_paragraph(self, rid: str) -> str:
        for para in self.paragraphs:
            flat = re.sub(r"\s+", " ", para).strip()
            if flat.startswith("|"):
                continue
            for m in BACKTICKED_ID_RE.finditer(flat):
                if m.group(1) != rid:
                    continue
                before = flat[:m.start()].rstrip()
                after = flat[m.end():]
                if (before == "" or before.endswith((".", ":", "—"))) and (
                    after.strip() == ""
                    or re.match(r"\s+[A-Z“\"]", after)
                    or re.match(r"\s*[-*]\s", after)
                ):
                    return flat
        return ""

    def is_normative_line(self, line: str) -> bool:
        """Notes, examples and rationale are set as block quotes; tables carry
        restatements whose wording §21.1 subordinates to the rule."""
        s = line.strip()
        return not (s.startswith(">") or s.startswith("|"))


# --------------------------------------------------------------------------
# CRC-32C — §4.5 fixes the parameters; Appendix B prints the check vectors.
# --------------------------------------------------------------------------

def _crc_table() -> list[int]:
    table = []
    for i in range(256):
        c = i
        for _ in range(8):
            c = (c >> 1) ^ (0x82F63B78 if c & 1 else 0)
        table.append(c)
    return table


_CRC_TABLE = _crc_table()


def crc32c(data: bytes) -> int:
    crc = 0xFFFFFFFF
    for b in data:
        crc = _CRC_TABLE[(crc ^ b) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF


# --------------------------------------------------------------------------
# Register checks
# --------------------------------------------------------------------------

def check_register(spec: Spec, report: Report) -> None:
    rows_by_prefix = spec.rows
    all_rows = [r for rows in rows_by_prefix.values() for r in rows]

    if not all_rows:
        report.add("REG-00", "error register present", ["§21.2–§21.5 hold no rows"])
        return

    # REG-01 -- row identifiers are positional labels; a hole or a repeat means
    # an edit shifted rows, which is how ADR-0049's damage entered.
    failures = []
    for prefix, rows in rows_by_prefix.items():
        got = [r["id"] for r in rows]
        want = [f"{prefix}{n}" for n in range(1, len(rows) + 1)]
        if got != want:
            missing = [w for w in want if w not in got]
            extra = [g for g in got if g not in want]
            failures.append(
                f"§21 {prefix}-rows are not contiguous: "
                f"{len(rows)} rows, missing {missing or 'none'}, unexpected {extra or 'none'}"
            )
    report.add("REG-01", "row ids contiguous", failures)

    # REG-02 -- two rows with identical condition text oblige two vectors with
    # nothing to tell them apart.
    seen: dict[str, list[str]] = defaultdict(list)
    for r in all_rows:
        seen[r["condition"]].append(r["id"])
    failures = [
        f"rows {', '.join(ids)} carry byte-identical condition text: {cond[:80]}…"
        for cond, ids in seen.items() if len(ids) > 1
    ]
    report.add("REG-02", "no duplicate condition text", failures)

    # REG-03 -- a row citing an identifier the document does not define sends a
    # vector author nowhere.
    known = set(spec.ids)
    failures = []
    for r in all_rows:
        for rid in ID_RE.findall(r["rule"]):
            if rid not in known:
                failures.append(f"{r['id']} cites {rid}, which this document does not define")
    report.add("REG-03", "governing rules resolve", failures)

    # REG-04 -- each subsection states its own row count.
    failures = []
    for prefix, heading, _ in REGISTER_SECTIONS:
        block = "\n".join(spec._section_lines(heading))
        stated = re.search(r"(\d+) conditions", block)
        actual = len(rows_by_prefix[prefix])
        if not stated:
            failures.append(f"{heading[5:9]} states no row count (nothing cross-checks it)")
        elif int(stated.group(1)) != actual:
            failures.append(
                f"{heading[5:9]} states {stated.group(1)} conditions, holds {actual}"
            )
    report.add("REG-04", "subsection counts agree", failures)

    # REG-05 -- §21.8's totals are the corpus's build list.
    total_rows = len(all_rows)
    total_instances = sum(spec.instance_count(r["instances"]) for r in all_rows)
    flat = re.sub(r"\s+", " ", spec.text)
    m = re.search(r"(\d+) conditions over ([\d,]+) named instances", flat)
    failures = []
    if not m:
        failures.append("§21.8 states no total")
    else:
        claimed_rows = int(m.group(1))
        claimed_inst = int(m.group(2).replace(",", ""))
        if claimed_rows != total_rows or claimed_inst != total_instances:
            failures.append(
                f"§21.8 claims {claimed_rows} conditions over {claimed_inst} instances; "
                f"the register holds {total_rows} over {total_instances}"
            )
    report.add("REG-05", "§21.8 total agrees", failures)

    # REG-06/07/08 -- the register's own vocabulary, and the invariant §21.1
    # states between the two columns.
    failures, warnings = [], []
    for r in all_rows:
        det = r["detector"].strip()
        if det not in VALID_DETECTORS:
            failures.append(f"{r['id']} has detector '{det}'")
        points = [p.strip() for p in re.split(r"[;,]", re.sub(r"\([^)]*\)", "", r["detected"]))]
        for p in filter(None, points):
            if p not in VALID_DETECTION_POINTS:
                failures.append(f"{r['id']} has detection point '{p}'")
        is_cert = "certification" in r["detected"]
        if det == "verifier" and not is_cert:
            failures.append(
                f"{r['id']} is verifier-detected but its detection point is "
                f"'{r['detected']}'; §21.1 places verifier rows at certification"
            )
        if det == "reader" and is_cert:
            failures.append(
                f"{r['id']} is reader-detected at certification, which §19.2 "
                f"places outside the reader tiers entirely"
            )
    report.add("REG-06", "detector and detection point", failures, warnings)

    # REG-07 -- §21.1's count is mechanical only while no cell hides a
    # semicolon inside a parenthetical.
    failures = []
    for r in all_rows:
        for group in re.findall(r"\([^)]*\)|\[[^\]]*\]", r["instances"]):
            if ";" in group:
                failures.append(
                    f"{r['id']} has a semicolon inside '{group}'; the mechanical "
                    f"count and the reading diverge"
                )
    report.add("REG-07", "instance cells count mechanically", failures)

    # REG-08 -- §21.1 makes completeness normative: "a violation this
    # specification names and the register omits is a defect in this document."
    #
    # Two senses of "cites" matter, and conflating them is how a missing row
    # hides. A row's *governing rule* is the backticked identifier; the bare
    # identifiers after it are supporting citations. An identifier that only
    # ever appears as support has no row of its own, however often it is
    # mentioned — which is precisely how the front-signature-block row went
    # missing while its rule stayed visible in a neighbouring row's
    # parenthetical.
    #
    # This is a heuristic over prose, so it warns rather than fails: a hit is a
    # question for a human, not a verdict.
    governing, supporting = set(), set()
    for r in all_rows:
        primary = re.match(r"\s*`\[(R-[A-Z]{3}-\d{2})\]`", r["rule"])
        if primary:
            governing.add(primary.group(1))
        for rid in ID_RE.findall(r["rule"]):
            if not primary or rid != primary.group(1):
                supporting.add(rid)

    warnings, dispositioned, stale = [], [], []
    for rid in spec.ids:
        if rid in governing or rid in WITHDRAWN_IDS:
            if rid in COMPLETENESS_DISPOSITIONED:
                stale.append(rid)
            continue
        para = spec.defining_paragraph(rid)
        if not para:
            continue
        if not re.search(
            r"validity error|reject-file|reject-layer|reject-tile|ignore-record", para
        ):
            if rid in COMPLETENESS_DISPOSITIONED:
                stale.append(rid)
            continue
        if rid in COMPLETENESS_DISPOSITIONED:
            dispositioned.append(rid)
        elif rid in supporting:
            warnings.append(
                f"{rid} names a violation but appears only as a supporting "
                f"citation; no row takes it as its governing rule"
            )
        else:
            warnings.append(
                f"{rid} names a violation and no register row cites it at all"
            )
    for rid in sorted(set(stale)):
        warnings.append(
            f"{rid} is dispositioned in COMPLETENESS_DISPOSITIONED but no longer "
            f"needs to be; drop the entry"
        )
    if dispositioned:
        warnings.append(
            f"({len(dispositioned)} rule(s) dispositioned as naming no file "
            f"condition: {', '.join(sorted(dispositioned))})"
        )
    report.add("REG-08", "register completeness (heuristic)", [], warnings)


# --------------------------------------------------------------------------
# Spec-wide checks
# --------------------------------------------------------------------------

def check_spec(spec: Spec, report: Report) -> None:
    # SPEC-01 -- §2.2: identifiers are stable and defined once.
    sites = spec.definition_sites()
    failures = []
    for rid in spec.ids:
        n = sites.get(rid, 0)
        if rid in WITHDRAWN_IDS:
            if n:
                failures.append(
                    f"{rid} is withdrawn ({WITHDRAWN_IDS[rid]}) but has {n} definition site(s)"
                )
        elif n != 1:
            failures.append(f"{rid} has {n} definition sites; §2.2 expects exactly one")
    report.add("SPEC-01", "requirement ids defined once", failures)

    # SPEC-02 -- a hole in a prefix's numbering is either a silent deletion or a
    # typo; §2.2 requires retirement to be recorded, so a hole must be declared.
    by_prefix: dict[str, list[int]] = defaultdict(list)
    for rid in spec.ids:
        by_prefix[rid[:5]].append(int(rid[-2:]))
    failures = []
    for prefix, numbers in sorted(by_prefix.items()):
        holes = [n for n in range(1, max(numbers) + 1) if n not in numbers]
        for n in holes:
            failures.append(
                f"{prefix}{n:02d} is absent, and no withdrawal is recorded for it"
            )
    report.add("SPEC-02", "requirement id numbering", failures)

    # SPEC-03 -- AGENTS.md rule 5.
    failures, warnings = [], []
    for i, line in enumerate(spec.lines, 1):
        if not spec.is_normative_line(line):
            continue
        for m in re.finditer(BCP14_VERBS, line):
            failures.append(f"line {i}: lowercase '{m.group(0)}' in normative text")
        for m in re.finditer(BCP14_ADJECTIVES, line):
            warnings.append(
                f"line {i}: lowercase '{m.group(0)}' — ordinary English, or a "
                f"BCP 14 keyword that lost its case?"
            )
    report.add("SPEC-03", "BCP 14 keywords are ALL CAPS", failures, warnings)

    # SPEC-04 -- vocabulary an ADR retired must not survive anywhere.
    failures = []
    for term, authority in RETIRED_TERMS.items():
        for i, line in enumerate(spec.lines, 1):
            if re.search(re.escape(term), line, re.I):
                failures.append(f"line {i}: retired term '{term}' ({authority})")
    report.add("SPEC-04", "retired terminology absent", failures)

    # SPEC-05 -- Appendix A prints bytes; the sections state rules. This
    # rebuilds the file from the rules and compares.
    failures = []
    printed = _appendix_a_bytes(spec)
    if printed is None:
        failures.append("Appendix A's hex dump could not be parsed")
    else:
        built = _build_minimal_file()
        if printed != built:
            first = next(
                (k for k in range(min(len(printed), len(built)))
                 if printed[k] != built[k]),
                min(len(printed), len(built)),
            )
            failures.append(
                f"Appendix A's dump ({len(printed)} B) differs from a file built "
                f"from the spec's rules ({len(built)} B); first difference at byte {first}"
            )
    report.add("SPEC-05", "Appendix A byte-exact", failures)

    # SPEC-06 -- Appendix B is a finding aid that restates constants defined
    # elsewhere. These are the ones a machine can recompute or cross-read.
    failures = _check_constants(spec)
    report.add("SPEC-06", "restated constants agree", failures)


def _appendix_a_bytes(spec: Spec) -> bytes | None:
    m = re.search(r"```\n(0000  89 54.*?)\n```", spec.text, re.S)
    if not m:
        return None
    body = re.sub(r"^\w{4}  ", "", m.group(1), flags=re.M)
    return bytes.fromhex("".join(re.findall(r"[0-9A-Fa-f]{2}", body)))


def _build_minimal_file() -> bytes:
    """The smallest conforming file, from §5.1, §6.1, §6.2, §7.1 and §4.5.

    Front signature block; a directory region holding a zero-length record
    sequence and its CRC-32C; the pre-trailer pad; the trailer. The file_id is
    the value Appendix A's annotation names, any nonzero value being conforming.
    """
    front = b"\x89TARN\r\n\x1a" + b"\x00" * 8
    directory = struct.pack("<I", crc32c(b""))          # §7.1 — CRC over zero bytes
    pad = b"\x00" * 44                                   # §5.2 — slack, zeroed by advice
    trailer = (
        b"\x8aNRAT\r\n\x1a"
        + struct.pack("<HHI", 1, 0, 0)                   # version_major/minor, flags
        + struct.pack("<QQQQQ", 1, 16, 4, 128, 0x0123456789ABCDEF)
        + b"\x00" * 4                                    # reserved
    )
    return front + directory + pad + trailer + struct.pack("<I", crc32c(trailer))


def _check_constants(spec: Spec) -> list[str]:
    failures = []
    flat = re.sub(r"\s+", " ", spec.text)

    def stated(pattern: str, label: str):
        m = re.search(pattern, flat)
        if not m:
            failures.append(f"{label} is not stated where this check expects it")
            return None
        return m.group(1)

    # Computable: §4.5's check vectors and §15.4's all-sentinel segment CRC.
    v = stated(r'CRC-32C\(`"123456789"`\) = `0x([0-9A-Fa-f]{8})`', "the CRC check vector")
    if v and int(v, 16) != crc32c(b"123456789"):
        failures.append(
            f"Appendix B states CRC-32C(\"123456789\") = 0x{v.upper()}; "
            f"§4.5's parameters give 0x{crc32c(b'123456789'):08X}"
        )
    seg = stated(r"CRC of a full all-sentinel segment \| `0x([0-9A-Fa-f]{8})`",
                 "the all-sentinel segment CRC")
    if seg:
        computed = crc32c((b"\xff" * 16 + b"\x00" * 4) * 65536)
        if int(seg, 16) != computed:
            failures.append(
                f"Appendix B states the all-sentinel segment CRC as 0x{seg.upper()}; "
                f"2¹⁶ sentinel entries give 0x{computed:08X}"
            )

    # Cross-read: the magics Appendix B restates against the sections that fix them.
    for label, section_pat, appendix_pat in (
        ("front signature magic",
         r"\| 0 \| 8 \| `(89 54 41 52 4E 0D 0A 1A)`",
         r"Front signature block \| `([0-9A-F ]+?)` \+"),
        ("trailer magic",
         r"\| 0 \| 8 \| bytes \| trailer magic \| structural \| `(8A 4E 52 41 54 0D 0A 1A)`",
         r"Trailer magic \| `([0-9A-F ]+?)` \|"),
    ):
        a = re.search(section_pat, flat)
        b = re.search(appendix_pat, flat)
        if a and b and a.group(1).strip() != b.group(1).strip():
            failures.append(
                f"{label}: the defining section says '{a.group(1)}', "
                f"Appendix B says '{b.group(1)}'"
            )
        elif not a or not b:
            failures.append(f"{label} could not be read from both places")

    # Sizes restated in Appendix B against the structures that fix them.
    for label, pat, want in (
        ("record header size", r"Record header size \| (\d+) bytes", 24),
        ("index entry size", r"Index entry size \| (\d+) bytes", 20),
        ("trailer size", r"Trailer size \| (\d+) bytes", 64),
        ("smallest conforming file", r"Smallest conforming file \| (\d+) bytes", 128),
    ):
        m = re.search(pat, flat)
        if not m:
            failures.append(f"{label} is not stated in Appendix B")
        elif int(m.group(1)) != want:
            failures.append(
                f"Appendix B states {label} as {m.group(1)}; the structure fixes {want}"
            )
    return failures


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def check_coverage(spec: Spec, root: Path, report: Report) -> None:
    """G5: every register instance has a vector (§21.8, `[R-ERR-02]`)."""
    import json

    mpath = root / "conformance" / "vectors" / "manifest.json"
    if not mpath.exists():
        report.add("COV-00", "corpus manifest present",
                   [f"{mpath} does not exist; the corpus has not been built"])
        return
    man = json.loads(mpath.read_text())
    vectors = man.get("vectors", [])

    # COV-01 -- every file the manifest names exists and matches its digest.
    import hashlib
    failures = []
    for v in vectors:
        p = mpath.parent / v["file"]
        if not p.exists():
            failures.append(f"{v['id']}: {v['file']} is missing")
            continue
        blob = p.read_bytes()
        if hashlib.sha256(blob).hexdigest() != v["sha256"]:
            failures.append(f"{v['id']}: {v['file']} does not match its recorded sha256")
        if len(blob) != v["size"]:
            failures.append(f"{v['id']}: {v['file']} is {len(blob)} B, manifest says {v['size']}")
    report.add("COV-01", "manifest matches the bytes", failures)

    # COV-04 -- two vectors with identical bytes and different claims is the
    # corpus contradicting itself; the review found exactly one such pair.
    seen: dict[str, list] = defaultdict(list)
    for v in vectors:
        seen[v["sha256"]].append(v)
    failures = []
    for digest, group in seen.items():
        if len(group) < 2:
            continue
        claims = {(g["conforming"],
                   tuple(sorted(x["row"] for x in g.get("violations", []))))
                  for g in group}
        ids = ", ".join(g["id"] for g in group)
        if len(claims) > 1:
            failures.append(
                f"{ids} are byte-identical but claim different things — "
                f"the corpus contradicts itself")
        else:
            failures.append(f"{ids} are byte-identical duplicates")
    report.add("COV-04", "no contradictory duplicates", failures)

    # COV-02 -- every row a vector cites still exists in the register.
    known = {r["id"] for rows in spec.rows.values() for r in rows}
    cited = {}
    failures = []
    for v in vectors:
        for viol in v.get("violations", []):
            cited.setdefault(viol["row"], []).append(v["id"])
            if viol["row"] not in known:
                failures.append(
                    f"{v['id']} cites register row {viol['row']}, which no longer exists")
    report.add("COV-02", "cited rows exist", failures)

    # COV-03 -- coverage itself. Reported, never failed: a partial corpus is
    # work in progress, and [R-ERR-02] makes a gap a gap, not a licence.
    total_rows = sum(len(r) for r in spec.rows.values())
    total_inst = sum(spec.instance_count(r["instances"])
                     for rows in spec.rows.values() for r in rows)
    covered_rows = len([r for r in known if r in cited])
    warnings = [
        f"rows with at least one vector: {covered_rows}/{total_rows}"
        f" ({covered_rows / total_rows * 100:.1f}%)",
        f"named instances in the register: {total_inst}; vectors so far: {len(vectors)}",
    ]
    per_class = defaultdict(int)
    malformed = []
    for v in vectors:
        if v["conforming"]:
            per_class["conforming"] += 1
            continue
        viol = (v.get("violations") or [{}])[0]
        outcome = viol.get("outcome")
        if not outcome:
            # A nonconforming vector with no outcome names no scope a reader
            # must refuse, so the manifest says nothing testable about it.
            malformed.append(f"{v['id']} is nonconforming but records no outcome")
            per_class["(no outcome)"] += 1
        else:
            per_class[outcome] += 1
    warnings.append("by class: "
                    + ", ".join(f"{k} {n}" for k, n in sorted(per_class.items())))
    report.add("COV-03", "register coverage", malformed, warnings)


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "spec" / "tarn.md").exists():
            return parent
    sys.exit("could not locate the repository root (no spec/tarn.md above this file)")


def load_spec(root: Path, rev: str | None) -> str:
    if rev is None:
        return (root / "spec" / "tarn.md").read_text()
    proc = subprocess.run(
        ["git", "-C", str(root), "show", f"{rev}:spec/tarn.md"],
        capture_output=True, text=True,
    )
    if proc.returncode:
        sys.exit(f"could not read spec/tarn.md at {rev}: {proc.stderr.strip()}")
    return proc.stdout


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Mechanical consistency checks for the TARN specification."
    )
    ap.add_argument("subcommand", nargs="?", default="all",
                    choices=["all", "register", "spec", "coverage"])
    ap.add_argument("--rev", help="check a git revision instead of the working tree")
    args = ap.parse_args(argv)

    root = repo_root()
    spec = Spec(load_spec(root, args.rev))
    where = args.rev or "working tree"
    print(f"tarn-check {args.subcommand} — spec/tarn.md at {where} "
          f"({len(spec.lines)} lines, {len(spec.ids)} requirement ids)\n")

    report = Report()
    if args.subcommand in ("all", "register"):
        check_register(spec, report)
    if args.subcommand in ("all", "spec"):
        check_spec(spec, report)
    if args.subcommand in ("all", "coverage"):
        check_coverage(spec, root, report)
    return report.render()


if __name__ == "__main__":
    raise SystemExit(main())
