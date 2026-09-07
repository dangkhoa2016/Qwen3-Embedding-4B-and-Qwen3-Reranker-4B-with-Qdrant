#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUDED_PREFIXES = (".github/ISSUE_TEMPLATE/",)


def replace_or_insert_switch(path: Path, expected: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        h1_index = next(i for i, line in enumerate(lines) if line.startswith("# "))
    except StopIteration as exc:
        raise SystemExit(f"missing H1 in bilingual Markdown file: {path.relative_to(ROOT)}") from exc

    switch_index = h1_index + 1
    if switch_index < len(lines) and lines[switch_index].startswith("> 🌐 Language / Ngôn ngữ:"):
        lines[switch_index] = expected
    else:
        lines.insert(switch_index, expected)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    normalized = 0
    for en in sorted(ROOT.rglob("*.md")):
        rel = str(en.relative_to(ROOT))
        if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            continue
        if en.name.endswith(".vi.md"):
            continue

        vi = en.with_name(en.name[:-3] + ".vi.md")
        if not vi.is_file():
            continue

        replace_or_insert_switch(
            en,
            f"> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt]({vi.name})",
        )
        replace_or_insert_switch(
            vi,
            f"> 🌐 Language / Ngôn ngữ: [English]({en.name}) | **Tiếng Việt**",
        )
        normalized += 1

    if normalized == 0:
        raise SystemExit("no bilingual Markdown pairs found")
    print(f"BILINGUAL_LANGUAGE_SWITCHES={normalized} PASS")


if __name__ == "__main__":
    main()
