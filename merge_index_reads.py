#!/usr/bin/env python3
"""Merge read_N.log (Cursor read_file style: '  N|line' + omission lines) into index.html."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent


def strip_read_file_block(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        if re.match(r"^\s*\.\.\.\s*\d+\s+lines not shown\s*\.\.\.\s*$", line):
            continue
        m = re.match(r"^(\s*)(\d+)\|(.*)$", line)
        if m:
            out.append(m.group(3))
        else:
            out.append(line)
    return "\n".join(out)


def main() -> None:
    parts = []
    paths = sorted(ROOT.glob("read_*.log"))
    if not paths:
        raise SystemExit("no read_*.log files")
    for p in paths:
        parts.append(strip_read_file_block(p.read_text(encoding="utf-8")))
    html = "\n".join(parts)
    html = html.rstrip() + "\n"
    if "</html>" not in html:
        raise SystemExit("merged HTML missing </html>")
    (ROOT / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
