#!/usr/bin/env python3
"""Merge Cursor read_file slices that use 'N|line' format; dedupe overlaps by line number."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def collect_numbered_lines(text: str) -> dict[int, str]:
    """Map 1-based line number -> content (last occurrence wins)."""
    out: dict[int, str] = {}
    for raw in text.splitlines():
        if re.match(r"^\s*\.\.\.\s*\d+\s+lines not shown\s*\.\.\.\s*$", raw):
            continue
        m = re.match(r"^\s*(\d+)\|(.*)$", raw)
        if not m:
            continue
        out[int(m.group(1))] = m.group(2)
    return out


def main() -> None:
    paths = sorted(ROOT.glob("chunk_*.txt"))
    if not paths:
        raise SystemExit("no chunk_*.txt under " + str(ROOT))
    merged: dict[int, str] = {}
    for p in paths:
        merged.update(collect_numbered_lines(p.read_text(encoding="utf-8")))
    if not merged:
        raise SystemExit("no numbered lines found in chunks")
    max_no = max(merged)
    missing = [n for n in range(1, max_no + 1) if n not in merged]
    if missing:
        raise SystemExit(f"missing line numbers: {missing[:20]}{'...' if len(missing) > 20 else ''}")
    lines = [merged[i] for i in range(1, max_no + 1)]
    html = "\n".join(lines).rstrip() + "\n"
    if not html.rstrip().endswith("</html>"):
        raise SystemExit("merged HTML does not end with </html>")
    (ROOT / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
