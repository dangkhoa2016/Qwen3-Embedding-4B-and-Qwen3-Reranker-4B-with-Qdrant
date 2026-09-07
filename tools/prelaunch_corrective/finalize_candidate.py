#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "MANIFEST.sha256"
CORRECTIVE_DIR = ROOT / "tools/prelaunch_corrective"


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def regenerate_manifest() -> int:
    tracked = run("git", "ls-files", "-z").split("\0")
    rows: list[tuple[str, str]] = []
    for rel in filter(None, tracked):
        if rel == "MANIFEST.sha256":
            continue
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"tracked file missing while freezing manifest: {rel}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append((rel, digest))
    rows.sort(key=lambda item: item[0].encode("utf-8"))
    MANIFEST.write_text("".join(f"{digest}  {rel}\n" for rel, digest in rows), encoding="utf-8")
    return len(rows)


def verify_manifest() -> None:
    subprocess.run(["sha256sum", "-c", "MANIFEST.sha256"], cwd=ROOT, check=True)


def main() -> None:
    if CORRECTIVE_DIR.exists():
        subprocess.run(["git", "rm", "-r", "tools/prelaunch_corrective"], cwd=ROOT, check=True)

    count = regenerate_manifest()
    subprocess.run(["git", "add", "MANIFEST.sha256"], cwd=ROOT, check=True)
    verify_manifest()

    status = run("git", "status", "--short")
    if not status:
        raise SystemExit("finalizer produced no tracked changes")
    print(status)
    print(f"FINAL_MANIFEST_ENTRIES={count}")
    print("CORRECTIVE_HARNESS_ABSENT=PASS")
    print("MANIFEST_FOR_CURRENT_WORKFLOW=PASS")
    print("FINAL_MANIFEST_VERIFY=PASS")


if __name__ == "__main__":
    main()
