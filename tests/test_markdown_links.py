from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def local_targets(path: Path):
    text = path.read_text(encoding="utf-8")
    for raw in LINK_RE.findall(text):
        target = raw.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        yield target


def test_all_relative_markdown_links_resolve():
    markdown = sorted(
        path for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and ".pytest_cache" not in path.parts
    )
    assert markdown
    failures = []
    for path in markdown:
        for target in local_targets(path):
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                failures.append((str(path.relative_to(ROOT)), target, "escapes repository"))
                continue
            if not resolved.exists():
                failures.append((str(path.relative_to(ROOT)), target, "missing"))
    assert not failures, failures
