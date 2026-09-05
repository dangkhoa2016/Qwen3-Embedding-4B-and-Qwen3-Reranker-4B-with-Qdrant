#!/usr/bin/env python3
from __future__ import annotations

import argparse
from email.parser import Parser
from pathlib import Path
import re
import tarfile
import zipfile

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 CI installs tomli
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]
IMPORT_NAME = "qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant"
EXPECTED_DOCS = (
    "README.md",
    "README.vi.md",
    "LICENSE",
    ".github/SECURITY.md",
    ".github/SECURITY.vi.md",
    ".github/CONTRIBUTING.md",
    ".github/CONTRIBUTING.vi.md",
    "docs/README.md",
    "docs/README.vi.md",
    "docs/releases/v1.0.0.md",
    "docs/releases/v1.0.0.vi.md",
)


def normalize_distribution(name: str) -> str:
    return re.sub(r"[-_.]+", "_", name).lower()


def load_identity() -> tuple[str, str]:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    return project["name"], project["version"]


def verify(dist_dir: Path) -> tuple[Path, Path]:
    distribution, version = load_identity()
    normalized = normalize_distribution(distribution)
    wheels = sorted(dist_dir.glob(f"{normalized}-{version}-*.whl"))
    sdists = sorted(dist_dir.glob(f"{normalized}-{version}.tar.gz"))
    if len(wheels) != 1:
        raise SystemExit(f"expected exactly one canonical wheel, found {len(wheels)}: {wheels}")
    if len(sdists) != 1:
        raise SystemExit(f"expected exactly one canonical sdist, found {len(sdists)}: {sdists}")
    wheel, sdist = wheels[0], sdists[0]

    with zipfile.ZipFile(wheel) as zf:
        names = set(zf.namelist())
        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            raise SystemExit(f"expected one wheel METADATA file, found {metadata_names}")
        metadata = Parser().parsestr(zf.read(metadata_names[0]).decode("utf-8"))
        assert metadata["Name"] == distribution, (metadata["Name"], distribution)
        assert metadata["Version"] == version, (metadata["Version"], version)
        assert metadata["License-Expression"] == "MIT", metadata["License-Expression"]
        assert f"{IMPORT_NAME}/__init__.py" in names
        assert any(name.endswith(".dist-info/licenses/LICENSE") for name in names)

    prefix = f"{normalized}-{version}/"
    with tarfile.open(sdist, "r:gz") as tf:
        names = set(tf.getnames())
        assert prefix + f"src/{IMPORT_NAME}/__init__.py" in names
        for path in EXPECTED_DOCS:
            assert prefix + path in names, path

    return wheel, sdist


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    wheel, sdist = verify(args.dist_dir)
    print(f"DISTRIBUTION_WHEEL={wheel.name} PASS")
    print(f"DISTRIBUTION_SDIST={sdist.name} PASS")
    print("DISTRIBUTION_METADATA=PASS")


if __name__ == "__main__":
    main()
