# Provenance của production demo
> 🌐 Language / Ngôn ngữ: [English](PRODUCTION_DEMO_PROVENANCE.md) | **Tiếng Việt**

Tài liệu này ghi public runtime, data và artifact identities cho production demo `1.0.0`.

## Release identity

```text
Package=qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant
Version=1.0.0
Author=Đăng Khoa <i.am@dangkhoa.dev>
License=MIT
```

Internal Python package namespace vẫn là `qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant`.

## Model và Kaggle input identities

```text
Embedding model=Qwen3-Embedding-4B
Embedding Kaggle input=dangkhoa2016/qwen-qwen3-embedding-4b
Embedding backend=Transformers / PyTorch CPU FP16

Reranker model=Qwen3-Reranker-4B
Reranker Kaggle input=dangkhoa2016/giladgd-qwen3-reranker-4b-gguf
Reranker format=GGUF Q4_K_M
Reranker GGUF SHA256=941f7d1d1524251c026a797b803ac9575545c5d7aa19b26e0e49661d7720af49

Hardened runtime Kaggle input=dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime
llama.cpp pin=b10699
llama launcher SHA256=28a79707376877f09065fa05fda5a9a6f57dfb4aed01c9918123667e38ae1f41
llama implementation SHA256=c4807f2f10cdf354270ac97c1f091d0846e8154749b4b8347f5f26a40184d425
```

## Qdrant data identity

```text
Qdrant Kaggle input=dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k
Qdrant version=1.18.3
collection=knowledge_entities_qwen3_4b_text_v21
points=20000
vector size=2560
distance=cosine
snapshot=knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot
snapshot size=283812352 bytes
snapshot SHA256=71f12fe14ef51966069347290ad15302d389e488d7904dab6cf0cf190f43064f
```

## Qualified behavior

- Retrieval default: `K=5`.
- Semantic validation: 3/3 pass.
- cgroup OOM và OOM-kill: zero.
- Qualified pipeline: `468.489s`.
- End-to-end Run All: `469.782s` trong threshold `600s`.
- Same-session repeated Run All: đã verify PASS bằng owned-process cleanup; process chưa được xác minh không bao giờ bị terminate tự động.

Xem `PRODUCTION_QUALIFICATION.vi.md`.
