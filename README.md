# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant
> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](README.vi.md)

[![CI](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml/badge.svg)](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml)

**Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant** is a production-oriented retrieval stack built around **Qwen3-Embedding-4B**, **Qwen3-Reranker-4B**, and Qdrant. It provides a CPU-oriented FastAPI service plus a reproducible bilingual 20K-point Qdrant production demo.

## What this project provides

- Bearer-authenticated REST APIs for Qwen3-Embedding-4B embeddings and Qwen3-Reranker-4B reranking.
- Qwen3-Embedding-4B through Transformers / PyTorch with the qualified CPU FP16 profile.
- Qwen3-Reranker-4B through Transformers for the general backend and GGUF `Q4_K_M` through the qualified hardened llama.cpp runtime for the production demo.
- Qdrant `1.18.3` with an immutable canonical 20K bilingual snapshot.
- Conservative CPU concurrency, memory-headroom, startup, readiness, request-size, and authentication gates.
- Bilingual reproducibility documentation and an executable Kaggle notebook.

Large model files, GGUF files, the hardened llama.cpp runtime, PyTorch, and the Qdrant snapshot are external inputs and are not bundled with the Python package.

## Production qualification

Fresh Kaggle CPU qualification of the publication-ready runtime path recorded:

```text
Production qualification: PASS
Semantic validation: 3/3 PASS
cgroup OOM events: 0
cgroup OOM-kill events: 0
Qualified pipeline: 468.489s
Verified Run All: 469.782s
Same-session rerun safety: PASS
Qualification threshold: 600s
Retrieval default: K=5
```

The timing result is specific to the qualified Kaggle CPU environment and is not a general performance guarantee.

## Architecture

```text
query
  -> Qwen3-Embedding-4B (Transformers / PyTorch CPU FP16)
  -> Qdrant 1.18.3 / canonical 20K bilingual snapshot
  -> Top-5 candidates
  -> Qwen3-Reranker-4B Q4_K_M (GGUF / qualified hardened llama.cpp)
  -> final ranked results
```

## Requirements

Python `>=3.10` is required. Install a host-appropriate PyTorch build separately.

The qualified Kaggle reproduction uses exactly four external inputs:

1. `dangkhoa2016/qwen-qwen3-embedding-4b` — Qwen3-Embedding-4B, Transformers `default`, Version `1`.
2. `dangkhoa2016/giladgd-qwen3-reranker-4b-gguf` — contains `Qwen3-Reranker-4B.Q4_K_M.gguf`.
3. `dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k` — contains `knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot`.
4. `dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime` — qualified hardened llama.cpp runtime for Qwen3-Reranker-4B.

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

For the GGUF backend:

```text
RERANKER_BACKEND=llama_cpp
RERANKER_GGUF_PATH=/absolute/path/to/Qwen3-Reranker-4B.Q4_K_M.gguf
LLAMA_SERVER_BIN=/absolute/path/to/llama-server-patched
```

Then:

```bash
set -a
source .env
set +a
bash scripts/start-server.sh
```

## API overview

Unauthenticated operational endpoints:

```text
GET /health
GET /ready
```

Bearer-authenticated endpoints:

```text
GET  /v1/models
GET  /v1/stats
POST /v1/embeddings
POST /v1/rerank
```

## Qualified Qdrant production demo

Use:

- `README_PRODUCTION_DEMO.md`
- `guide-production-demo.md`
- `notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb`
- `PRODUCTION_QUALIFICATION.md`
- `PRODUCTION_DEMO_PROVENANCE.md`

Verified Qdrant contract:

```text
Qdrant version: 1.18.3
Collection: knowledge_entities_qwen3_4b_text_v21
Points: 20000
Vector size: 2560
Distance: cosine
Retrieval default: K=5
```

## Development and verification

```bash
python scripts/check-canonical-model-naming.py .
python scripts/validate-publication-notebook.py notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb
PYTHONPATH=src pytest -q
python -m compileall -q src scripts tools tests
```

## Security

Read `SECURITY.md` before deployment or vulnerability reporting.

## Contributing

See `CONTRIBUTING.md`. Qualification-sensitive behavior changes require fresh evidence.

## Known limitations

- The qualified timing baseline is Kaggle-CPU-specific.
- Loading 4B-class models is memory intensive.
- The package does not bundle model weights, GGUF files, PyTorch, Qdrant data, or the hardened llama.cpp runtime.
- The qualified CPU profile uses conservative single-inference concurrency.

## Reproducibility and provenance

Qualification results are in `PRODUCTION_QUALIFICATION.md`; runtime/data identities are in `PRODUCTION_DEMO_PROVENANCE.md`.

## License

MIT License. See `LICENSE`.
