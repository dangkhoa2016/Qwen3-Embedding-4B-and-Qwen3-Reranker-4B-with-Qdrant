# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant — v1.0.0
> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](RELEASE_NOTES_v1.0.0.vi.md)

**Project:** **Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant**  
**Python distribution:** `qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant==1.0.0`  
**Git tag:** `v1.0.0`

`1.0.0` is the first public release.

## Highlights

- CPU-oriented FastAPI service for Qwen3-Embedding-4B embeddings and Qwen3-Reranker-4B reranking.
- Qualified Qwen3-Embedding-4B Transformers / PyTorch CPU FP16 path.
- Qualified Qwen3-Reranker-4B `Q4_K_M` GGUF path through the pinned hardened llama.cpp runtime.
- Qdrant `1.18.3` canonical 20K bilingual snapshot.
- Reproducible four-input Kaggle production demo.

## Production qualification

- Fresh Kaggle CPU qualification: **PASS**.
- Semantic validation: **3/3 PASS**.
- cgroup OOM events: **0**.
- cgroup OOM-kill events: **0**.
- Qualified pipeline: `468.489s`.
- End-to-end Run All: `469.782s`, within `600s`.
- Same-session repeated Run All: **PASS** with fail-closed owned-process cleanup.
- Default retrieval depth: `K=5`.

## Verification

GitHub CI verifies Python 3.10 and 3.12, the blocking regression suite, canonical model naming, publication-ready notebook structure, source manifest integrity, and wheel/sdist construction.

## Packaging and deployment

Python distribution: `qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant==1.0.0`. The wheel filename uses the normalized stem `qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant` as required by Python packaging conventions.

Model weights, GGUF files, PyTorch, the hardened llama.cpp runtime, and the Qdrant snapshot are external inputs and are not bundled.

See `PRODUCTION_QUALIFICATION.md` and `PRODUCTION_DEMO_PROVENANCE.md`.

## Publication channels

```text
Source repository: GitHub
Release identity: v1.0.0
GitHub Release: tagged release channel for canonical release assets
Package index / PyPI: separate publication channel
```

Publication through one channel does not imply publication through another; each channel is verified independently.
