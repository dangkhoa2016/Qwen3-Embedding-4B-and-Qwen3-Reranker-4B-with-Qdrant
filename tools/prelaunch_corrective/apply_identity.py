#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD_DIST = "qwen3" + "-embedding-4b-reranker-4b-qdrant"
NEW_DIST = "qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant"
OLD_STEM = "qwen3" + "_embedding_4b_reranker_4b_qdrant"
NEW_STEM = "qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant"
OLD_IMPORT = "qwen3" + "_qdrant"
NEW_IMPORT = NEW_STEM

ACTION_REPLACEMENTS = {
    "actions/checkout@" + "3d3c42e5aac5ba805825da76410c181273ba90b1 # v7": "actions/checkout@v7",
    "actions/setup-python@" + "5fda3b95a4ea91299a34e894583c3862153e4b97 # v7": "actions/setup-python@v7",
    "actions/upload-artifact@" + "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7": "actions/upload-artifact@v7",
}


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if any(part in {".venv", "venv", "__pycache__", ".pytest_cache", "dist", "build"} for part in path.parts):
            continue
        data = path.read_bytes()
        if b"\0" in data[:8192]:
            continue
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        files.append(path)
    return files


def replace_text(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = text.replace(OLD_DIST, NEW_DIST).replace(OLD_STEM, NEW_STEM).replace(OLD_IMPORT, NEW_IMPORT)
    for old, new in ACTION_REPLACEMENTS.items():
        updated = updated.replace(old, new)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    old_package = ROOT / "src" / OLD_IMPORT
    new_package = ROOT / "src" / NEW_IMPORT
    if old_package.exists() and not new_package.exists():
        old_package.rename(new_package)
    elif old_package.exists() and new_package.exists():
        raise SystemExit("both old and new package directories exist")

    changed = 0
    for path in iter_text_files():
        changed += int(replace_text(path))

    init_path = new_package / "__init__.py"
    if not init_path.is_file():
        raise SystemExit(f"missing canonical package: {init_path}")
    init_path.write_text(
        '__version__ = "1.0.0"\n'
        '__project_name__ = "Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant"\n'
        '__project_slug__ = "Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant"\n'
        '__distribution_name__ = "qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant"\n'
        '__display_name__ = __project_name__\n',
        encoding="utf-8",
    )

    print(f"IDENTITY_MIGRATION_TEXT_FILES_CHANGED={changed}")
    print(f"CANONICAL_IMPORT_NAMESPACE={NEW_IMPORT}")


if __name__ == "__main__":
    main()
