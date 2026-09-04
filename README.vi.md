# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant
> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

[![CI](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml/badge.svg)](https://github.com/dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant/actions/workflows/ci.yml)

## Tổng quan

**Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant** là stack retrieval và reranking song ngữ định hướng production, kết hợp **Qwen3-Embedding-4B**, **Qwen3-Reranker-4B** và **Qdrant**. Dự án cung cấp FastAPI service có authentication cùng production demo Kaggle theo hướng CPU, có khả năng tái hiện trên canonical bilingual Qdrant snapshot 20.000 điểm.

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
curl -fsS   -H "Authorization: Bearer $DUAL_API_KEY"   http://127.0.0.1:8000/v1/models
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
