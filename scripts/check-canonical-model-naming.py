#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
family = "Qwen" + "3"
standalone = re.compile(r"(?<![-\w])" + family + r"(?![-\w])")

internal_tokens = [
    "Stage" + "-II",
    "STAGE" + "2",
    "v0." + "2.3c",
    "0.2." + "3rc1",
    "DIAG" + "_CELL3",
    "v7 " + "diagnostics",
    "mount " + "corrective",
    "v8-" + "mount-corrective",
]

if (root / ".git").exists():
    tracked = subprocess.check_output(["git", "ls-files"], cwd=root, text=True).splitlines()
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"], cwd=root, text=True
    ).splitlines()
    rels = sorted(set(tracked + untracked))
else:
    rels = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())

violations = []
for rel in rels:
    p = root / rel
    if not p.is_file():
        continue
    data = p.read_bytes()
    if b"\0" in data[:8192]:
        continue
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        continue

    for lineno, line in enumerate(text.splitlines(), 1):
        if standalone.search(line):
            violations.append(f"{rel}:{lineno}: standalone model-family token: {line.strip()}")
        if not rel.startswith("tests/"):
            for token in internal_tokens:
                if token in line:
                    violations.append(f"{rel}:{lineno}: internal publication token {token!r}: {line.strip()}")

if violations:
    print("CANONICAL_MODEL_NAMING_GUARD=FAIL")
    for v in violations:
        print(v)
    raise SystemExit(1)

print("CANONICAL_MODEL_NAMING_GUARD=PASS")
print("PUBLICATION_INTERNAL_TERMS_GUARD=PASS")
