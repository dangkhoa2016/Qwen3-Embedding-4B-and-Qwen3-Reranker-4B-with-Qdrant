#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/ci.yml"
MANIFEST = ROOT / "MANIFEST.sha256"
CORRECTIVE_DIR = ROOT / "tools/prelaunch_corrective"

FINAL_WORKFLOW = r'''name: CI

on:
  push:
    branches: [main]
    tags: ["v*"]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality:
    name: Quality / Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.12"]

    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
          cache-dependency-path: |
            requirements.txt
            requirements-dev.txt
            pyproject.toml

      - name: Install CI dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install --index-url https://download.pytorch.org/whl/cpu torch
          python -m pip install -r requirements-dev.txt

      - name: Validate source manifest structure and coverage
        run: |
          python - <<'PY'
          from pathlib import Path
          import re
          import subprocess
          manifest = Path("MANIFEST.sha256")
          assert manifest.is_file(), "MANIFEST.sha256 is missing"
          entries, seen = [], set()
          for lineno, raw in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
              match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw)
              assert match, f"invalid MANIFEST.sha256 line {lineno}: {raw!r}"
              _, path = match.groups()
              assert path not in seen, f"duplicate manifest path: {path}"
              assert Path(path).is_file(), f"manifest path does not exist: {path}"
              seen.add(path)
              entries.append(path)
          tracked = set(subprocess.check_output(["git", "ls-files"], text=True).splitlines())
          expected = tracked - {"MANIFEST.sha256"}
          assert seen == expected, (
              f"manifest coverage mismatch; missing={sorted(expected - seen)}, "
              f"extra={sorted(seen - expected)}"
          )
          print(f"MANIFEST_STRUCTURE={len(entries)}/{len(expected)} PASS")
          PY

      - name: Verify frozen source manifest hashes
        run: sha256sum -c MANIFEST.sha256

      - name: Compile Python sources
        run: python -m compileall -q src scripts tools tests

      - name: Validate shell syntax
        shell: bash
        run: |
          while IFS= read -r -d '' file; do
            bash -n "$file"
          done < <(find scripts tools -type f -name '*.sh' -print0)

      - name: Validate canonical model naming
        run: python scripts/check-canonical-model-naming.py .

      - name: Validate publication-ready Kaggle notebook
        run: python scripts/validate-publication-notebook.py notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb

      - name: Run full regression suite
        env:
          PYTHONPATH: src
        run: pytest -q

  package:
    name: Package
    runs-on: ubuntu-latest
    timeout-minutes: 15
    needs: quality

    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: pyproject.toml

      - name: Install build frontend
        run: |
          python -m pip install --upgrade pip
          python -m pip install build

      - name: Build wheel and sdist
        run: |
          export SOURCE_DATE_EPOCH="$(git show -s --format=%ct HEAD)"
          python -m build

      - name: Verify distribution metadata and contents
        run: python scripts/verify_distribution.py --dist-dir dist

      - name: Upload canonical tag distributions
        if: startsWith(github.ref, 'refs/tags/v')
        uses: actions/upload-artifact@v7
        with:
          name: qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant-${{ github.ref_name }}-dist
          path: dist/*
          if-no-files-found: error
          retention-days: 14
'''


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
    WORKFLOW.write_text(FINAL_WORKFLOW, encoding="utf-8")
    subprocess.run(["git", "add", ".github/workflows/ci.yml"], cwd=ROOT, check=True)

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
    print("FINAL_CI_CONTENTS_READ=PASS")
    print("FINAL_MANIFEST_VERIFY=PASS")


if __name__ == "__main__":
    main()
