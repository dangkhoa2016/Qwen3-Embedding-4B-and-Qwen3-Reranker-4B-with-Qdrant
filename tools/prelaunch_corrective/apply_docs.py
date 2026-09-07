#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]

MOVES = {
    "CONTRIBUTING.md": ".github/CONTRIBUTING.md",
    "CONTRIBUTING.vi.md": ".github/CONTRIBUTING.vi.md",
    "SECURITY.md": ".github/SECURITY.md",
    "SECURITY.vi.md": ".github/SECURITY.vi.md",
    "README_PRODUCTION_DEMO.md": "docs/production-demo/overview.md",
    "README_PRODUCTION_DEMO.vi.md": "docs/production-demo/overview.vi.md",
    "guide-production-demo.md": "docs/production-demo/guide.md",
    "guide-production-demo.vi.md": "docs/production-demo/guide.vi.md",
    "PRODUCTION_QUALIFICATION.md": "docs/production-demo/qualification.md",
    "PRODUCTION_QUALIFICATION.vi.md": "docs/production-demo/qualification.vi.md",
    "PRODUCTION_DEMO_PROVENANCE.md": "docs/production-demo/provenance.md",
    "PRODUCTION_DEMO_PROVENANCE.vi.md": "docs/production-demo/provenance.vi.md",
    "RELEASE_NOTES_v1.0.0.md": "docs/releases/v1.0.0.md",
    "RELEASE_NOTES_v1.0.0.vi.md": "docs/releases/v1.0.0.vi.md",
}

DISPLAY = "Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant"

README_EN = f'''# {DISPLAY}
> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

[![CI](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml/badge.svg)](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml)

## Overview

**{DISPLAY}** is a production-oriented bilingual retrieval and reranking stack that combines **Qwen3-Embedding-4B**, **Qwen3-Reranker-4B**, and **Qdrant**. It provides an authenticated FastAPI service and a reproducible CPU-focused Kaggle production demo backed by a canonical 20,000-point bilingual Qdrant snapshot.

The Python distribution is `qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant`. Model weights, GGUF files, PyTorch, the hardened llama.cpp runtime, and the Qdrant snapshot remain external inputs rather than package payloads.

## Architecture

```text
query
  -> Qwen3-Embedding-4B (Transformers / PyTorch CPU FP16)
  -> Qdrant 1.18.3 / canonical 20K bilingual snapshot
  -> Top-5 candidates
  -> Qwen3-Reranker-4B Q4_K_M (GGUF / hardened llama.cpp)
  -> final ranked results
```

The production profile deliberately uses conservative CPU concurrency and fail-closed startup, readiness, request-size, authentication, and process-ownership gates.

## Capabilities

- Bearer-authenticated REST APIs for embeddings and reranking.
- Qwen3-Embedding-4B via Transformers / PyTorch using the qualified CPU FP16 profile.
- Qwen3-Reranker-4B through the Transformers backend and the qualified `Q4_K_M` GGUF + hardened llama.cpp production path.
- Qdrant `1.18.3` with an immutable canonical 20K bilingual snapshot.
- Safe repeated **Run All** behavior with verified-owned process cleanup.
- Bilingual project, production-demo, qualification, provenance, security, and contributing documentation.
- Reproducible wheel/sdist builds and CI validation on Python 3.10 and 3.12.

## Production qualification

The qualified Kaggle CPU publication path recorded:

```text
Production qualification: PASS
Semantic validation: 3/3 PASS
cgroup OOM events: 0
cgroup OOM-kill events: 0
Qualified pipeline: 468.489s
Verified Run All: 469.782s
Qualification threshold: 600s
Retrieval default: K=5
```

These timings describe the qualified Kaggle CPU environment; they are not a general performance guarantee. See [Production qualification](docs/production-demo/qualification.md) for the acceptance record.

## Requirements and external inputs

Python `>=3.10` is required. Install a host-appropriate PyTorch build separately.

The qualified Kaggle reproduction uses exactly four external inputs:

1. `dangkhoa2016/qwen-qwen3-embedding-4b` — Qwen3-Embedding-4B, Transformers `default`, Version `1`.
2. `dangkhoa2016/giladgd-qwen3-reranker-4b-gguf` — contains `Qwen3-Reranker-4B.Q4_K_M.gguf`.
3. `dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k` — contains `knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot`.
4. `dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime` — pinned hardened llama.cpp runtime.

Verified production data/runtime identities are documented in [Provenance](docs/production-demo/provenance.md).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

For development:

```bash
python -m pip install -r requirements-dev.txt
```

## Quick start

Create local configuration:

```bash
cp .env.example .env
```

Set at least:

```text
DUAL_API_KEY=<strong-random-secret>
EMBEDDING_MODEL_PATH=/absolute/path/to/Qwen3-Embedding-4B
RERANKER_MODEL_PATH=/absolute/path/to/Qwen3-Reranker-4B
MAX_INSTRUCTION_CHARS=1024
```

For the qualified GGUF reranker path:

```text
RERANKER_BACKEND=llama_cpp
RERANKER_GGUF_PATH=/absolute/path/to/Qwen3-Reranker-4B.Q4_K_M.gguf
LLAMA_SERVER_BIN=/absolute/path/to/llama-server-patched
```

Start the service:

```bash
set -a
source .env
set +a
bash scripts/start-server.sh
```

## API overview

Operational endpoints do not require bearer authentication:

```text
GET /health
GET /ready
```

Application endpoints require bearer authentication:

```text
GET  /v1/models
GET  /v1/stats
POST /v1/embeddings
POST /v1/rerank
```

Example health check:

```bash
curl -fsS http://127.0.0.1:8000/health
```

Example authenticated model listing:

```bash
curl -fsS \
  -H "Authorization: Bearer $DUAL_API_KEY" \
  http://127.0.0.1:8000/v1/models
```

## Production demo

The production demo restores the frozen Qdrant snapshot rather than reseeding or re-embedding the 20K collection. Its verified contract is:

```text
Qdrant version: 1.18.3
Collection: knowledge_entities_qwen3_4b_text_v21
Points: 20000
Vector size: 2560
Distance: cosine
Retrieval default: K=5
```

Start with [Production demo](docs/production-demo/overview.md) and follow the [Execution guide](docs/production-demo/guide.md). The executable notebook is `notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb`.

## Reproducibility and provenance

The project freezes the canonical Qdrant snapshot, Qwen3-Reranker-4B GGUF digest, hardened llama.cpp runtime identities, production retrieval depth, and qualification outcomes. See [Production qualification](docs/production-demo/qualification.md) and [Provenance](docs/production-demo/provenance.md).

## Documentation

The complete documentation index is available at [Documentation](docs/README.md).

Key entry points:

- [Production demo](docs/production-demo/overview.md)
- [Execution guide](docs/production-demo/guide.md)
- [Production qualification](docs/production-demo/qualification.md)
- [Provenance](docs/production-demo/provenance.md)
- [Production roadmap](docs/production-demo/roadmap.md)
- [v1.0.0 release notes](docs/releases/v1.0.0.md)
- [Security](.github/SECURITY.md)
- [Contributing](.github/CONTRIBUTING.md)

## Development and verification

```bash
python scripts/check-canonical-model-naming.py .
python scripts/validate-publication-notebook.py notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb
PYTHONPATH=src pytest -q
python -m compileall -q src scripts tools tests
```

Package/publication changes also require source-manifest and wheel/sdist verification.

## Security

Review [Security](.github/SECURITY.md) before deployment or vulnerability reporting. Never expose model/runtime endpoints publicly without appropriate authentication and operational controls.

## Contributing

See [Contributing](.github/CONTRIBUTING.md). Changes to qualification-sensitive behavior require fresh evidence appropriate to the change.

## Known limitations

- Loading 4B-class models is memory intensive.
- The qualified timing baseline is specific to the Kaggle CPU environment.
- The production profile deliberately uses conservative single-inference concurrency.
- Model weights, GGUF files, PyTorch, Qdrant data, and the hardened llama.cpp runtime are not bundled.
- This repository provides a production-style reproducible demo, not a continuously hosted HA/SLA service.

## Release

The first public release is `v1.0.0`. Read the [v1.0.0 release notes](docs/releases/v1.0.0.md) and use the GitHub tagged release as the canonical release-asset channel.

## License

MIT License. See [LICENSE](LICENSE).
'''

README_VI = f'''# {DISPLAY}
> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

[![CI](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml/badge.svg)](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml)

## Tổng quan

**{DISPLAY}** là stack retrieval và reranking song ngữ định hướng production, kết hợp **Qwen3-Embedding-4B**, **Qwen3-Reranker-4B** và **Qdrant**. Dự án cung cấp FastAPI service có authentication cùng production demo Kaggle theo hướng CPU, có khả năng tái hiện trên canonical bilingual Qdrant snapshot 20.000 điểm.

Python distribution là `qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant`. Model weights, GGUF files, PyTorch, hardened llama.cpp runtime và Qdrant snapshot vẫn là external inputs thay vì được bundle vào package.

## Kiến trúc

```text
query
  -> Qwen3-Embedding-4B (Transformers / PyTorch CPU FP16)
  -> Qdrant 1.18.3 / canonical 20K bilingual snapshot
  -> Top-5 candidates
  -> Qwen3-Reranker-4B Q4_K_M (GGUF / hardened llama.cpp)
  -> final ranked results
```

Production profile chủ đích dùng CPU concurrency bảo thủ cùng các gate fail-closed cho startup, readiness, request size, authentication và process ownership.

## Khả năng

- REST API có bearer authentication cho embedding và reranking.
- Qwen3-Embedding-4B qua Transformers / PyTorch với qualified CPU FP16 profile.
- Qwen3-Reranker-4B qua Transformers backend và qualified `Q4_K_M` GGUF + hardened llama.cpp production path.
- Qdrant `1.18.3` với immutable canonical bilingual snapshot 20K điểm.
- **Run All** lặp lại an toàn với verified-owned process cleanup.
- Tài liệu song ngữ cho project, production demo, qualification, provenance, security và contributing.
- Wheel/sdist có khả năng tái hiện và CI validation trên Python 3.10/3.12.

## Kiểm chứng production

Qualified Kaggle CPU publication path ghi nhận:

```text
Production qualification: PASS
Semantic validation: 3/3 PASS
cgroup OOM events: 0
cgroup OOM-kill events: 0
Qualified pipeline: 468.489s
Verified Run All: 469.782s
Qualification threshold: 600s
Retrieval default: K=5
```

Timing chỉ mô tả qualified Kaggle CPU environment, không phải cam kết hiệu năng chung. Xem [Kiểm chứng production](docs/production-demo/qualification.vi.md) để đọc acceptance record.

## Yêu cầu và external inputs

Yêu cầu Python `>=3.10`. Cài PyTorch build phù hợp với host riêng.

Qualified Kaggle reproduction dùng đúng bốn external inputs:

1. `dangkhoa2016/qwen-qwen3-embedding-4b` — Qwen3-Embedding-4B, Transformers `default`, Version `1`.
2. `dangkhoa2016/giladgd-qwen3-reranker-4b-gguf` — chứa `Qwen3-Reranker-4B.Q4_K_M.gguf`.
3. `dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k` — chứa `knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot`.
4. `dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime` — pinned hardened llama.cpp runtime.

Các identity production data/runtime đã verify nằm trong [Nguồn gốc](docs/production-demo/provenance.vi.md).

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

Cho development:

```bash
python -m pip install -r requirements-dev.txt
```

## Khởi động nhanh

Tạo local configuration:

```bash
cp .env.example .env
```

Đặt ít nhất:

```text
DUAL_API_KEY=<strong-random-secret>
EMBEDDING_MODEL_PATH=/absolute/path/to/Qwen3-Embedding-4B
RERANKER_MODEL_PATH=/absolute/path/to/Qwen3-Reranker-4B
MAX_INSTRUCTION_CHARS=1024
```

Với qualified GGUF reranker path:

```text
RERANKER_BACKEND=llama_cpp
RERANKER_GGUF_PATH=/absolute/path/to/Qwen3-Reranker-4B.Q4_K_M.gguf
LLAMA_SERVER_BIN=/absolute/path/to/llama-server-patched
```

Khởi động service:

```bash
set -a
source .env
set +a
bash scripts/start-server.sh
```

## Tổng quan API

Operational endpoints không cần bearer authentication:

```text
GET /health
GET /ready
```

Application endpoints cần bearer authentication:

```text
GET  /v1/models
GET  /v1/stats
POST /v1/embeddings
POST /v1/rerank
```

Ví dụ health check:

```bash
curl -fsS http://127.0.0.1:8000/health
```

Ví dụ authenticated model listing:

```bash
curl -fsS \
  -H "Authorization: Bearer $DUAL_API_KEY" \
  http://127.0.0.1:8000/v1/models
```

## Production demo

Production demo restore frozen Qdrant snapshot thay vì seed hoặc re-embed collection 20K. Contract đã verify:

```text
Qdrant version: 1.18.3
Collection: knowledge_entities_qwen3_4b_text_v21
Points: 20000
Vector size: 2560
Distance: cosine
Retrieval default: K=5
```

Bắt đầu tại [Production demo](docs/production-demo/overview.vi.md) và làm theo [Hướng dẫn thực thi](docs/production-demo/guide.vi.md). Executable notebook là `notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb`.

## Khả năng tái hiện và nguồn gốc

Dự án đóng băng canonical Qdrant snapshot, Qwen3-Reranker-4B GGUF digest, hardened llama.cpp runtime identities, production retrieval depth và qualification outcomes. Xem [Kiểm chứng production](docs/production-demo/qualification.vi.md) và [Nguồn gốc](docs/production-demo/provenance.vi.md).

## Tài liệu

Documentation index đầy đủ nằm tại [Tài liệu](docs/README.vi.md).

Các entry point chính:

- [Production demo](docs/production-demo/overview.vi.md)
- [Hướng dẫn thực thi](docs/production-demo/guide.vi.md)
- [Kiểm chứng production](docs/production-demo/qualification.vi.md)
- [Nguồn gốc](docs/production-demo/provenance.vi.md)
- [Production roadmap](docs/production-demo/roadmap.vi.md)
- [Release notes v1.0.0](docs/releases/v1.0.0.vi.md)
- [Bảo mật](.github/SECURITY.vi.md)
- [Đóng góp](.github/CONTRIBUTING.vi.md)

## Phát triển và kiểm chứng

```bash
python scripts/check-canonical-model-naming.py .
python scripts/validate-publication-notebook.py notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb
PYTHONPATH=src pytest -q
python -m compileall -q src scripts tools tests
```

Package/publication changes cũng phải verify source manifest và wheel/sdist.

## Bảo mật

Đọc [Bảo mật](.github/SECURITY.vi.md) trước deployment hoặc vulnerability reporting. Không expose model/runtime endpoints công khai nếu thiếu authentication và operational controls phù hợp.

## Đóng góp

Xem [Đóng góp](.github/CONTRIBUTING.vi.md). Thay đổi behavior nhạy cảm với qualification cần fresh evidence phù hợp.

## Hạn chế đã biết

- Load model cỡ 4B tốn nhiều RAM.
- Qualified timing baseline phụ thuộc Kaggle CPU environment.
- Production profile chủ đích dùng conservative single-inference concurrency.
- Package không bundle model weights, GGUF files, PyTorch, Qdrant data hoặc hardened llama.cpp runtime.
- Repo cung cấp production-style reproducible demo, không phải dịch vụ HA/SLA được host liên tục.

## Phát hành

First public release là `v1.0.0`. Đọc [Release notes v1.0.0](docs/releases/v1.0.0.vi.md) và dùng GitHub tagged release làm canonical release-asset channel.

## Giấy phép

MIT License. Xem [LICENSE](LICENSE).
'''

DOCS_EN = '''# Documentation
> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

This index collects the public documentation for **Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant**.

## Production demo

- [Overview](production-demo/overview.md)
- [Execution guide](production-demo/guide.md)
- [Production qualification](production-demo/qualification.md)
- [Provenance](production-demo/provenance.md)
- [Roadmap](production-demo/roadmap.md)

## Release

- [v1.0.0 release notes](releases/v1.0.0.md)

## Project governance

- [Security](../.github/SECURITY.md)
- [Contributing](../.github/CONTRIBUTING.md)
- [Support](../.github/SUPPORT.md)
- [Code of Conduct](../.github/CODE_OF_CONDUCT.md)

Return to the [project README](../README.md).
'''

DOCS_VI = '''# Tài liệu
> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

Đây là documentation index công khai cho **Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant**.

## Production demo

- [Tổng quan](production-demo/overview.vi.md)
- [Hướng dẫn thực thi](production-demo/guide.vi.md)
- [Kiểm chứng production](production-demo/qualification.vi.md)
- [Nguồn gốc](production-demo/provenance.vi.md)
- [Roadmap](production-demo/roadmap.vi.md)

## Phát hành

- [Release notes v1.0.0](releases/v1.0.0.vi.md)

## Governance

- [Bảo mật](../.github/SECURITY.vi.md)
- [Đóng góp](../.github/CONTRIBUTING.vi.md)
- [Hỗ trợ](../.github/SUPPORT.vi.md)
- [Quy tắc ứng xử](../.github/CODE_OF_CONDUCT.vi.md)

Quay lại [README dự án](../README.vi.md).
'''


def git_mv(src: str, dst: str) -> None:
    source, target = ROOT / src, ROOT / dst
    if target.exists() and not source.exists():
        return
    if not source.exists():
        raise SystemExit(f"missing source for documentation move: {src}")
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", src, dst], cwd=ROOT, check=True)


def replace(path: Path, replacements: dict[str, str]) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def normalize_moved_docs() -> None:
    overview = ROOT / "docs/production-demo/overview.md"
    overview_vi = ROOT / "docs/production-demo/overview.vi.md"
    if overview.is_file():
        text = overview.read_text(encoding="utf-8")
        lines = text.splitlines()
        if lines:
            lines[0] = f"# {DISPLAY} - Production Demo"
        text = "\n".join(lines) + "\n"
        text = text.replace("[Tiếng Việt](README_PRODUCTION_DEMO.vi.md)", "[Tiếng Việt](overview.vi.md)")
        text = text.replace("`PRODUCTION_QUALIFICATION.md`", "[Production qualification](qualification.md)")
        text = text.replace("`PRODUCTION_DEMO_PROVENANCE.md`", "[Provenance](provenance.md)")
        overview.write_text(text, encoding="utf-8")
    if overview_vi.is_file():
        text = overview_vi.read_text(encoding="utf-8")
        lines = text.splitlines()
        if lines:
            lines[0] = f"# {DISPLAY} - Production Demo"
        text = "\n".join(lines) + "\n"
        text = text.replace("[English](README_PRODUCTION_DEMO.md)", "[English](overview.md)")
        text = text.replace("`PRODUCTION_QUALIFICATION.vi.md`", "[Kiểm chứng production](qualification.vi.md)")
        text = text.replace("`PRODUCTION_DEMO_PROVENANCE.vi.md`", "[Nguồn gốc](provenance.vi.md)")
        overview_vi.write_text(text, encoding="utf-8")

    for name in ("guide.md", "qualification.md", "provenance.md", "roadmap.md"):
        path = ROOT / "docs/production-demo" / name
        replace(path, {
            "guide-production-demo.vi.md": name.replace(".md", ".vi.md") if name == "guide.md" else "guide.vi.md",
            "PRODUCTION_QUALIFICATION.md": "qualification.md",
            "PRODUCTION_DEMO_PROVENANCE.md": "provenance.md",
        })
    for name in ("guide.vi.md", "qualification.vi.md", "provenance.vi.md", "roadmap.vi.md"):
        path = ROOT / "docs/production-demo" / name
        replace(path, {
            "guide-production-demo.md": "guide.md",
            "PRODUCTION_QUALIFICATION.vi.md": "qualification.vi.md",
            "PRODUCTION_DEMO_PROVENANCE.vi.md": "provenance.vi.md",
        })


def normalize_release_notes() -> None:
    for name, counterpart in (("v1.0.0.md", "v1.0.0.vi.md"), ("v1.0.0.vi.md", "v1.0.0.md")):
        path = ROOT / "docs/releases" / name
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if lines:
            lines[0] = f"# {DISPLAY} - v1.0.0"
        text = "\n".join(lines) + "\n"
        text = text.replace("RELEASE_NOTES_v1.0.0.vi.md", counterpart).replace("RELEASE_NOTES_v1.0.0.md", counterpart)
        text = text.replace("See `PRODUCTION_QUALIFICATION.md` and `PRODUCTION_DEMO_PROVENANCE.md`.", "See [Production qualification](../production-demo/qualification.md) and [Provenance](../production-demo/provenance.md).")
        text = text.replace("Xem `PRODUCTION_QUALIFICATION.vi.md` và `PRODUCTION_DEMO_PROVENANCE.vi.md`.", "Xem [Kiểm chứng production](../production-demo/qualification.vi.md) và [Nguồn gốc](../production-demo/provenance.vi.md).")
        filtered = []
        skipping = False
        for line in text.splitlines():
            if line.startswith("## Publication channels") or line.startswith("## Kênh phát hành"):
                skipping = True
                continue
            if skipping:
                continue
            if "PyPI" in line:
                continue
            filtered.append(line)
        path.write_text("\n".join(filtered).rstrip() + "\n", encoding="utf-8")


def update_path_dependent_sources() -> None:
    replacements = {
        'ROOT / "SECURITY.md"': 'ROOT / ".github" / "SECURITY.md"',
        'ROOT / "SECURITY.vi.md"': 'ROOT / ".github" / "SECURITY.vi.md"',
        'read("PRODUCTION_QUALIFICATION.md")': 'read("docs/production-demo/qualification.md")',
        'read("RELEASE_NOTES_v1.0.0.md")': 'read("docs/releases/v1.0.0.md")',
        'read("RELEASE_NOTES_v1.0.0.vi.md")': 'read("docs/releases/v1.0.0.vi.md")',
        '"README_PRODUCTION_DEMO.md"': '"docs/production-demo/overview.md"',
        '"README_PRODUCTION_DEMO.vi.md"': '"docs/production-demo/overview.vi.md"',
        '"guide-production-demo.md"': '"docs/production-demo/guide.md"',
        '"guide-production-demo.vi.md"': '"docs/production-demo/guide.vi.md"',
        '"PRODUCTION_QUALIFICATION.md"': '"docs/production-demo/qualification.md"',
        '"PRODUCTION_QUALIFICATION.vi.md"': '"docs/production-demo/qualification.vi.md"',
        '"PRODUCTION_DEMO_PROVENANCE.md"': '"docs/production-demo/provenance.md"',
        '"PRODUCTION_DEMO_PROVENANCE.vi.md"': '"docs/production-demo/provenance.vi.md"',
        '"RELEASE_NOTES_v1.0.0.md"': '"docs/releases/v1.0.0.md"',
        '"RELEASE_NOTES_v1.0.0.vi.md"': '"docs/releases/v1.0.0.vi.md"',
    }
    for path in [*ROOT.glob("tests/*.py"), *ROOT.glob("scripts/*.py"), *ROOT.glob("scripts/*.sh"), *ROOT.glob("tools/*.py"), *ROOT.glob("tools/*.sh")]:
        replace(path, replacements)


def update_manifest_in() -> None:
    path = ROOT / "MANIFEST.in"
    path.write_text(
        "include README.vi.md\n"
        "include .github/SECURITY.md\n"
        "include .github/SECURITY.vi.md\n"
        "include .github/CONTRIBUTING.md\n"
        "include .github/CONTRIBUTING.vi.md\n"
        "recursive-include docs *.md\n",
        encoding="utf-8",
    )


def main() -> None:
    for src, dst in MOVES.items():
        git_mv(src, dst)
    (ROOT / "docs/releases").mkdir(parents=True, exist_ok=True)
    (ROOT / "docs/README.md").write_text(DOCS_EN, encoding="utf-8")
    (ROOT / "docs/README.vi.md").write_text(DOCS_VI, encoding="utf-8")
    (ROOT / "README.md").write_text(README_EN, encoding="utf-8")
    (ROOT / "README.vi.md").write_text(README_VI, encoding="utf-8")
    normalize_moved_docs()
    normalize_release_notes()
    update_path_dependent_sources()
    update_manifest_in()
    print("DOCUMENTATION_TOPOLOGY_TRANSFORM=PASS")


if __name__ == "__main__":
    main()
