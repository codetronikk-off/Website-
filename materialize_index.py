#!/usr/bin/env python3
"""Join chunk_*.txt (Cursor read_file slices) into index.html."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def normalize_block(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if re.match(r"^\s*\.\.\.\s*\d+\s+lines not shown\s*\.\.\.\s*$", line):
            continue
        m = re.match(r"^\s*\d+\|(.*)$", line)
        lines.append(m.group(1) if m else line)
    return "\n".join(lines)


def main() -> None:
    chunks = sorted(ROOT.glob("chunk_*.txt"))
    if not chunks:
        raise SystemExit("no chunk_*.txt under " + str(ROOT))
    html = "\n".join(normalize_block(p.read_text(encoding="utf-8")) for p in chunks)
    html = html.rstrip() + "\n"
    if not html.rstrip().endswith("</html>"):
        raise SystemExit("merged HTML does not end with </html>")
    (ROOT / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
