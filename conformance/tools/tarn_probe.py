#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""Measure the cold remote-open cost of a TARN file — gate G4.

§6.4 states the accounting: "The baseline remote open is two requests, each
with an exact target… A reader MAY instead speculatively fetch a suffix window
in one request and use containment." §19.1 adds that the open "consumes the
trailer and directory only… so its I/O is §6.4's request accounting at any
layer count and file size."

This measures that claim against a deliberately dumb HTTP server. What it
contains is a **prober**, not a reader: it performs §19.1's open — trailer,
directory, record walk far enough to count layers — and stops. It fetches no
tile index, decodes no payload, returns no sample, and pronounces no file
conforming or nonconforming. ADR-0052 fixes that boundary; the reason for it is
ADR-0046's, that a reader living in this repository would become the de facto
definition of conformance.

    python3 tarn_probe.py            # run the matrix, print the table
    python3 tarn_probe.py --markdown # emit the table as the G4 record
"""

from __future__ import annotations

import http.server
import socket
import struct
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tarn_build import Channel, Layer, build, crc32c, minimal  # noqa: E402

WINDOW = 65_536  # §6.4's discovery window; writer advice, not a reader limit


# --------------------------------------------------------------------------
# A deliberately dumb HTTP server: byte ranges, and nothing else.
# --------------------------------------------------------------------------

@dataclass
class ServerBehaviour:
    """Transports vary; §6.4 and [R-CNT-10] anticipate these three."""
    suffix_ranges: bool = True     # honours `Range: bytes=-N`
    ranges: bool = True            # honours Range at all; False ⇒ always 200
    expose_length: bool = True     # sends Content-Length on a HEAD


class _Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):  # silence
        pass

    def _blob(self) -> bytes | None:
        return self.server.blobs.get(self.path)

    def do_HEAD(self):
        blob = self._blob()
        if blob is None:
            self.send_error(404); return
        self.server.log.append(("HEAD", self.path, None))
        self.send_response(200)
        if self.server.behaviour.expose_length:
            self.send_header("Content-Length", str(len(blob)))
        self.send_header("Accept-Ranges",
                         "bytes" if self.server.behaviour.ranges else "none")
        self.end_headers()

    def do_GET(self):
        blob = self._blob()
        if blob is None:
            self.send_error(404); return
        rng = self.headers.get("Range")
        beh = self.server.behaviour
        self.server.log.append(("GET", self.path, rng))

        if rng and beh.ranges:
            spec = rng.split("=", 1)[1].strip()
            if spec.startswith("-"):
                if not beh.suffix_ranges:
                    # A transport with no suffix-range support: [R-CNT-10]
                    # requires the reader to fall back, not to guess.
                    self.send_error(416); return
                start, end = max(0, len(blob) - int(spec[1:])), len(blob) - 1
            else:
                a, _, b = spec.partition("-")
                start = int(a)
                end = int(b) if b else len(blob) - 1
                end = min(end, len(blob) - 1)
            body = blob[start:end + 1]
            self.send_response(206)
            self.send_header("Content-Range",
                             f"bytes {start}-{end}/{len(blob)}")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # No Range, or a server that ignores it: 200 with the whole body.
        self.send_response(200)
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)


class DumbServer:
    def __init__(self, blobs: dict[str, bytes], behaviour: ServerBehaviour):
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self.httpd.blobs = blobs
        self.httpd.behaviour = behaviour
        self.httpd.log = []
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start(); return self

    def __exit__(self, *a):
        self.httpd.shutdown(); self.httpd.server_close()

    @property
    def port(self) -> int:
        return self.httpd.server_address[1]

    def reset(self):
        self.httpd.log = []

    @property
    def requests(self) -> list:
        return self.httpd.log


# --------------------------------------------------------------------------
# The prober: §19.1's open, and not one byte further.
# --------------------------------------------------------------------------

@dataclass
class Probe:
    requests: int = 0
    bytes_fetched: int = 0
    layers: int = 0
    notes: list[str] = field(default_factory=list)
    failed: str | None = None


class _Client:
    def __init__(self, port: int, path: str, probe: Probe):
        self.port, self.path, self.probe = port, path, probe

    def _http(self, method: str, headers: dict[str, str]) -> tuple[int, dict, bytes]:
        self.probe.requests += 1
        with socket.create_connection(("127.0.0.1", self.port)) as s:
            req = f"{method} {self.path} HTTP/1.1\r\nHost: 127.0.0.1\r\n"
            for k, v in headers.items():
                req += f"{k}: {v}\r\n"
            req += "Connection: close\r\n\r\n"
            s.sendall(req.encode())
            buf = b""
            while True:
                chunk = s.recv(65536)
                if not chunk:
                    break
                buf += chunk
        head, _, body = buf.partition(b"\r\n\r\n")
        lines = head.decode("latin1").split("\r\n")
        status = int(lines[0].split()[1])
        hdrs = {}
        for line in lines[1:]:
            k, _, v = line.partition(":")
            hdrs[k.strip().lower()] = v.strip()
        self.probe.bytes_fetched += len(body)
        return status, hdrs, body

    def head(self):
        return self._http("HEAD", {})

    def range(self, spec: str):
        return self._http("GET", {"Range": f"bytes={spec}"})


def _parse_trailer(t: bytes) -> dict:
    """§6.2's gates, in the order [R-CNT-06] fixes."""
    if len(t) != 64 or t[:8] != b"\x8aNRAT\r\n\x1a":
        raise ValueError("trailer magic")
    if crc32c(t[:60]) != struct.unpack("<I", t[60:64])[0]:
        raise ValueError("trailer CRC")
    vmaj, vmin, flags = struct.unpack("<HHI", t[8:16])
    if vmaj == 0:
        raise ValueError("version_major 0")
    if vmaj != 1:
        raise ValueError(f"unimplemented format major {vmaj}")
    if flags & 0xFFFF:
        raise ValueError("unimplemented incompat flag")
    do, dl, cfl, fid = struct.unpack("<QQQQ", t[16:48])
    if fid == 0 or do < 16 or dl < 4 or cfl % 64 or t[48:60] != b"\x00" * 12:
        raise ValueError("trailer field gate")
    return dict(dir_offset=do, dir_length=dl, F=cfl, file_id=fid)


def _walk_directory(region: bytes) -> int:
    """§7.1 CRC, then §7.2's framing far enough to count layer records."""
    if crc32c(region[:-4]) != struct.unpack("<I", region[-4:])[0]:
        raise ValueError("directory CRC")
    seq, p, layers = region[:-4], 0, 0
    while p < len(seq):
        ty, fl, il, eo, el = struct.unpack("<HHIQQ", seq[p:p + 24])
        if ty == 0:
            raise ValueError("record type 0")
        if ty == 1:
            layers += 1
        p += 24 + il
    if p != len(seq):
        raise ValueError("record sequence residue")
    return layers


def probe(port: int, path: str, mode: str) -> Probe:
    """Perform §19.1's open and stop. `mode` selects the transport strategy."""
    pr = Probe()
    c = _Client(port, path, pr)
    try:
        if mode == "exact":
            # §6.4 request 1: the final 64 bytes.
            st, h, body = c.range("-64")
            if st == 200:
                # [R-CNT-10]: accept the full body deliberately, never treat a
                # prefix as the requested range.
                pr.notes.append("200 to a range request; accepted whole body")
                size = len(body)
                trailer = body[-64:]
                info = _parse_trailer(trailer)
                if info["F"] != size:
                    raise ValueError("committed_file_length != transport size")
                pr.layers = _walk_directory(
                    body[info["dir_offset"]:info["dir_offset"] + info["dir_length"]])
                return pr
            size = int(h["content-range"].split("/")[1])
            info = _parse_trailer(body)
            if info["F"] != size:
                raise ValueError("committed_file_length != transport size")
            # §6.4 request 2: the directory region, exactly.
            d0, dl = info["dir_offset"], info["dir_length"]
            _, _, region = c.range(f"{d0}-{d0 + dl - 1}")
            pr.layers = _walk_directory(region)

        elif mode == "speculative":
            st, h, body = c.range(f"-{WINDOW}")
            if st == 200:
                pr.notes.append("200 to a range request; accepted whole body")
                size = len(body); base = 0; buf = body
            else:
                size = int(h["content-range"].split("/")[1])
                base = int(h["content-range"].split()[1].split("-")[0])
                buf = body
            info = _parse_trailer(buf[-64:])
            if info["F"] != size:
                raise ValueError("committed_file_length != transport size")
            d0, dl = info["dir_offset"], info["dir_length"]
            if d0 >= base:                       # containment: no second request
                region = buf[d0 - base:d0 - base + dl]
                pr.notes.append("directory contained in the suffix window")
            else:
                pr.notes.append("directory outside the window; second request")
                _, _, region = c.range(f"{d0}-{d0 + dl - 1}")
            pr.layers = _walk_directory(region)

        elif mode == "exact-no-suffix":
            # §19.1 read literally on a transport with no suffix ranges: step 1
            # obtains F, step 2 fetches [F−64, F), step 3 fetches the directory.
            # Three round trips, violating nothing — see the G4 record.
            _, h, _ = c.head()
            size = int(h["content-length"])
            _, _, trailer = c.range(f"{size - 64}-{size - 1}")
            info = _parse_trailer(trailer)
            if info["F"] != size:
                raise ValueError("committed_file_length != transport size")
            d0, dl = info["dir_offset"], info["dir_length"]
            _, _, region = c.range(f"{d0}-{d0 + dl - 1}")
            pr.layers = _walk_directory(region)
            pr.notes.append("§19.1 taken literally: size probe, trailer, directory")

        elif mode == "no-suffix":
            # [R-CNT-10]: "SHOULD fall back to a size probe plus an absolute
            # range on transports without suffix-range support".
            _, h, _ = c.head()
            size = int(h["content-length"])
            start = max(0, size - WINDOW)
            _, _, buf = c.range(f"{start}-{size - 1}")
            info = _parse_trailer(buf[-64:])
            if info["F"] != size:
                raise ValueError("committed_file_length != transport size")
            d0, dl = info["dir_offset"], info["dir_length"]
            if d0 >= start:
                region = buf[d0 - start:d0 - start + dl]
                pr.notes.append("directory contained in the window")
            else:
                pr.notes.append("directory outside the window; extra request")
                _, _, region = c.range(f"{d0}-{d0 + dl - 1}")
            pr.layers = _walk_directory(region)
        else:
            raise ValueError(mode)
    except Exception as exc:                      # a failed open is a result
        pr.failed = str(exc)
    return pr


# --------------------------------------------------------------------------
# The cases
# --------------------------------------------------------------------------

def _empty_layer(nm: str) -> Layer:
    """A layer with extent 0: valid, zero addressed tiles (§11.1)."""
    return Layer(nm, extents=(0,), tile_extents=(1,), dim_names=("t",))


def _window_of(blob: bytes) -> int:
    """F − dir_offset: the suffix a speculative reader must fetch to contain
    the directory. §6.4's writer SHOULD is that this stay within 65,536."""
    return len(blob) - struct.unpack("<Q", blob[-40:-32])[0]


def _tune_window(want_inside: bool) -> tuple[bytes, int]:
    """Build a many-layer file whose window sits as close to §6.4's 65,536 as
    the structures allow, on the requested side of it.

    Coarse search over the layer count, then a fine search over the last
    layer's name length (§4.6 allows 1–255 bytes), which moves the directory a
    byte at a time. Empty layers keep dir_offset at 16, so the window is a
    clean function of directory size.
    """
    def make(n: int, tail: int) -> bytes:
        layers = [_empty_layer(f"layer{i:05d}") for i in range(n - 1)]
        layers.append(_empty_layer("z" * tail))
        return build(layers)

    n = 2
    while _window_of(make(n, 1)) <= WINDOW and n < 4000:
        n += 1
    # n is now the first layer count whose window exceeds 65,536 at tail = 1.
    best = None
    for cand_n in (n - 1, n):
        for tail in range(1, 256):
            blob = make(cand_n, tail)
            w = _window_of(blob)
            inside = w <= WINDOW
            if inside != want_inside:
                continue
            if best is None or abs(w - WINDOW) < abs(best[1] - WINDOW):
                best = (blob, w)
    return best


def cases() -> list[tuple[str, str, bytes]]:
    out = []
    out.append(("A", "Appendix A's minimal file, no layers", minimal()))
    out.append(("B", "one layer, 4 stored tiles",
                build([Layer("a", tiles=[bytes([16 * t + i for i in range(4)])
                                         for t in range(4)])])))
    fit, w_fit = _tune_window(want_inside=True)
    out.append(("C", f"directory just inside the window (F−dir_offset = {w_fit:,})", fit))
    over, w_over = _tune_window(want_inside=False)
    out.append(("D", f"directory just outside the window (F−dir_offset = {w_over:,})", over))
    big = build([Layer("big", extents=(4096, 4096), tile_extents=(4096, 4096),
                       channels=[Channel("v", 6)])])
    out.append(("E", f"one 16 MiB tile, file {len(big):,} B", big))
    out.append(("F", "512 layers",
                build([_empty_layer(f"L{i:04d}") for i in range(512)])))
    return out


MODES = [("exact", ServerBehaviour()),
         ("speculative", ServerBehaviour()),
         ("no-suffix", ServerBehaviour(suffix_ranges=False)),
         ("exact", ServerBehaviour(ranges=False)),
         ("exact-no-suffix", ServerBehaviour(suffix_ranges=False))]
MODE_LABEL = ["M1 exact-target", "M2 speculative suffix",
              "M3 no suffix-range, windowed", "M4 server ignores Range (200)",
              "M5 no suffix-range, §19.1 literal"]


def run() -> list[dict]:
    rows = []
    built = cases()
    blobs = {f"/{cid}.tarn": blob for cid, _, blob in built}
    for (mode, beh), label in zip(MODES, MODE_LABEL):
        with DumbServer(blobs, beh) as srv:
            for cid, desc, blob in built:
                pr = probe(srv.port, f"/{cid}.tarn", mode)
                rows.append(dict(case=cid, desc=desc, size=len(blob), mode=label,
                                 requests=pr.requests, bytes=pr.bytes_fetched,
                                 layers=pr.layers, failed=pr.failed,
                                 notes="; ".join(pr.notes)))
    return rows


def main() -> int:
    rows = run()
    md = "--markdown" in sys.argv
    sizes = {r["case"]: r["size"] for r in rows}
    descs = {}
    for r in rows:
        descs.setdefault(r["case"], r["desc"])
    if md:
        print("| Case | File | Size (B) | Mode | Requests | Bytes fetched | Layers |")
        print("|---|---|---|---|---|---|---|")
        for r in rows:
            v = r["failed"] or r["requests"]
            print(f"| {r['case']} | {r['desc']} | {r['size']:,} | {r['mode']} "
                  f"| {v} | {r['bytes']:,} | {r['layers']:,} |")
    else:
        for cid in sizes:
            print(f"\n{cid}  {descs[cid]}   ({sizes[cid]:,} bytes)")
            for r in rows:
                if r["case"] != cid:
                    continue
                v = f"FAILED: {r['failed']}" if r["failed"] else \
                    f"{r['requests']} request(s), {r['bytes']:,} B, {r['layers']:,} layers"
                print(f"    {r['mode']:<32} {v}")
                if r["notes"]:
                    print(f"        {r['notes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
