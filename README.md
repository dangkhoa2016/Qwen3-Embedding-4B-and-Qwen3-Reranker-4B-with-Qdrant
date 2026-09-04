# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant
> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

[![CI](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml/badge.svg)](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml)

## Overview

**Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant** is a production-oriented bilingual retrieval and reranking stack that combines **Qwen3-Embedding-4B**, **Qwen3-Reranker-4B**, and **Qdrant**. It provides an authenticated FastAPI service and a reproducible CPU-focused Kaggle production demo backed by a canonical 20,000-point bilingual Qdrant snapshot.

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
curl -fsS   -H "Authorization: Bearer $DUAL_API_KEY"   http://127.0.0.1:8000/v1/models
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
