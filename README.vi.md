# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant
> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

**Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant** là retrieval stack định hướng production, xây quanh **Qwen3-Embedding-4B**, **Qwen3-Reranker-4B** và Qdrant. Dự án cung cấp FastAPI service theo hướng CPU cùng production demo Qdrant song ngữ 20K point có khả năng tái hiện.

## Dự án cung cấp những gì

- REST API có bearer authentication cho embeddings của Qwen3-Embedding-4B và reranking của Qwen3-Reranker-4B.
- Qwen3-Embedding-4B qua Transformers / PyTorch với qualified CPU FP16 profile.
- Qwen3-Reranker-4B qua Transformers cho backend chung và GGUF `Q4_K_M` qua qualified hardened llama.cpp runtime cho production demo.
- Qdrant `1.18.3` với immutable canonical bilingual snapshot 20K point.
- Các gate bảo thủ cho CPU concurrency, memory-headroom, startup, readiness, request-size và authentication.
- Tài liệu reproducibility song ngữ và Kaggle notebook thực thi được.

Model files lớn, GGUF files, hardened llama.cpp runtime, PyTorch và Qdrant snapshot là external inputs, không bundle trong Python package.

## Kiểm chứng production

Fresh Kaggle CPU qualification của publication-ready runtime path ghi nhận:

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

Timing chỉ áp dụng cho qualified Kaggle CPU environment, không phải cam kết hiệu năng chung.

## Kiến trúc

```text
query
  -> Qwen3-Embedding-4B (Transformers / PyTorch CPU FP16)
  -> Qdrant 1.18.3 / canonical 20K bilingual snapshot
  -> Top-5 candidates
  -> Qwen3-Reranker-4B Q4_K_M (GGUF / qualified hardened llama.cpp)
  -> final ranked results
```

## Yêu cầu

Yêu cầu Python `>=3.10`. Cài PyTorch phù hợp với host riêng.

Qualified Kaggle reproduction dùng đúng bốn external inputs:

1. `dangkhoa2016/qwen-qwen3-embedding-4b` — Qwen3-Embedding-4B, Transformers `default`, Version `1`.
2. `dangkhoa2016/giladgd-qwen3-reranker-4b-gguf` — chứa `Qwen3-Reranker-4B.Q4_K_M.gguf`.
3. `dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k` — chứa `knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot`.
4. `dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime` — qualified hardened llama.cpp runtime cho Qwen3-Reranker-4B.

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

Development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

## Khởi động nhanh

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

Với GGUF backend:

```text
RERANKER_BACKEND=llama_cpp
RERANKER_GGUF_PATH=/absolute/path/to/Qwen3-Reranker-4B.Q4_K_M.gguf
LLAMA_SERVER_BIN=/absolute/path/to/llama-server-patched
```

## Tổng quan API

Operational endpoints không cần auth:

```text
GET /health
GET /ready
```

Endpoints cần bearer auth:

```text
GET  /v1/models
GET  /v1/stats
POST /v1/embeddings
POST /v1/rerank
```

## Qualified Qdrant production demo

Dùng:

- `README_PRODUCTION_DEMO.vi.md`
- `guide-production-demo.vi.md`
- `notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb`
- `PRODUCTION_QUALIFICATION.vi.md`
- `PRODUCTION_DEMO_PROVENANCE.vi.md`

Verified Qdrant contract:

```text
Qdrant version: 1.18.3
Collection: knowledge_entities_qwen3_4b_text_v21
Points: 20000
Vector size: 2560
Distance: cosine
Retrieval default: K=5
```

## Development và verification

```bash
python scripts/check-canonical-model-naming.py .
python scripts/validate-publication-notebook.py notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb
PYTHONPATH=src pytest -q
python -m compileall -q src scripts tools tests
```

## Bảo mật

Đọc `SECURITY.vi.md` trước deployment hoặc báo vulnerability.

## Đóng góp

Xem `CONTRIBUTING.vi.md`. Thay đổi behavior nhạy cảm với qualification cần fresh evidence.

## Hạn chế đã biết

- Qualified timing baseline phụ thuộc Kaggle CPU.
- Load model cỡ 4B tốn nhiều RAM.
- Package không bundle model weights, GGUF files, PyTorch, Qdrant data hoặc hardened llama.cpp runtime.
- Qualified CPU profile dùng conservative single-inference concurrency.

## Khả năng tái hiện và nguồn gốc

Qualification results nằm trong `PRODUCTION_QUALIFICATION.vi.md`; runtime/data identities nằm trong `PRODUCTION_DEMO_PROVENANCE.vi.md`.

## Giấy phép

MIT License. Xem `LICENSE`.
