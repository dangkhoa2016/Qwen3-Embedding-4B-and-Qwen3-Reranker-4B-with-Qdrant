# Qwen3-Embedding-4B / Qwen3-Reranker-4B and Qdrant Stack - v1.0.0
> 🌐 Language / Ngôn ngữ: [English](README_PRODUCTION_DEMO.md) | **Tiếng Việt**

Production demo chạy qualified retrieval path:

```text
query
  -> Qwen3-Embedding-4B (Transformers CPU FP16)
  -> Qdrant 1.18.3 / canonical 20K bilingual collection
  -> Top-5 candidates
  -> Qwen3-Reranker-4B Q4_K_M (qualified hardened llama.cpp runtime)
  -> final ranked results
```

## Cấu hình đã kiểm chứng

```text
RETRIEVAL_TOP_K=5
RERANK_TOP_K=5
DISPLAY_TOP_K=5
LLAMA_SERVER_THREADS=2
TORCH_NUM_THREADS=2
```

Fresh Kaggle qualification pass 3/3 semantic cases, zero cgroup OOM/OOM-kill, qualified pipeline `468.489s`, notebook total `469.782s`, nằm trong threshold `600s`.

## Kaggle inputs bắt buộc

1. `dangkhoa2016/qwen-qwen3-embedding-4b`
2. `dangkhoa2016/giladgd-qwen3-reranker-4b-gguf` có `Qwen3-Reranker-4B.Q4_K_M.gguf`
3. `dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k` có `knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot`
4. `dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime` có `RUNTIME-MANIFEST.sha256` và complete eight-file hardened runtime bundle

Kaggle mount datasets dưới `/kaggle/input/datasets/<owner>/<slug>` và models dưới `/kaggle/input/models/<owner>/<slug>/...`. Notebook kiểm tra exact canonical runtime path trước, chỉ dùng fail-closed recursive lookup bên trong `/kaggle/input/datasets` khi cần.

Snapshot:

```text
size=283812352 bytes
SHA256=71f12fe14ef51966069347290ad15302d389e488d7904dab6cf0cf190f43064f
```

Reranker GGUF SHA-256:

```text
941f7d1d1524251c026a797b803ac9575545c5d7aa19b26e0e49661d7720af49
```

Runtime identities:

```text
launcher SHA256=28a79707376877f09065fa05fda5a9a6f57dfb4aed01c9918123667e38ae1f41
mapped implementation SHA256=c4807f2f10cdf354270ac97c1f091d0846e8154749b4b8347f5f26a40184d425
```

Mở `notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb`, attach đủ bốn inputs, chọn CPU (`Accelerator: None`) với Internet On, sau đó **Restart Session → Run All**.

## Reproducibility pins

- Qdrant: `1.18.3`
- Qwen3-Reranker-4B GGUF: `Q4_K_M`
- llama.cpp pin: `b10699`
- Qdrant collection: `knowledge_entities_qwen3_4b_text_v21`
- Retrieval default: `K=5`

Xem `PRODUCTION_QUALIFICATION.vi.md` và `PRODUCTION_DEMO_PROVENANCE.vi.md`.

## Run All lặp lại an toàn

Trước khi start services, notebook kiểm tra state từ lần chạy trước trong cùng Kaggle session. Notebook chỉ terminate process có ownership được chứng minh bằng PID/`/proc` evidence, process identity, expected ports, working directory hoặc storage path và frozen Qwen3-Reranker-4B launcher identity. Nếu required port do process chưa được xác minh chiếm, notebook fail closed và không kill process đó.
