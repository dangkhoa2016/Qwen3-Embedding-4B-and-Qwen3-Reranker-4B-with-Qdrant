# Production qualification
> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](qualification.vi.md)

This document records the public production-demo qualification reference for `qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant` `1.0.0`.

## Qualification result

```text
Production qualification: PASS
Source ref: v1.0.0
Source head: 7616ef375044696cefbf949e186edc1a8f423680
Retrieval default: K=5
Semantic validation: 3/3 PASS
cgroup OOM events: 0
cgroup OOM-kill events: 0
Qualified pipeline: 468.489s
Run All threshold: 600s
Verified Run All: 469.782s
Same-session rerun safety: PASS
```

The timing applies only to the qualified Kaggle CPU environment.

## Semantic validation

1. `Which Southeast Asian country uses the baht?` → `Thailand`.
2. `Thủ đô của Nhật Bản là thành phố nào?` → `Tokyo`.
3. `Which country has thủ đô Bangkok and uses đồng baht?` → `Thailand`.

## Runtime and data identities

```text
Qdrant version=1.18.3
collection=knowledge_entities_qwen3_4b_text_v21
points=20000
vector size=2560
distance=cosine

snapshot SHA256=71f12fe14ef51966069347290ad15302d389e488d7904dab6cf0cf190f43064f
reranker GGUF SHA256=941f7d1d1524251c026a797b803ac9575545c5d7aa19b26e0e49661d7720af49
llama launcher SHA256=28a79707376877f09065fa05fda5a9a6f57dfb4aed01c9918123667e38ae1f41
llama implementation SHA256=c4807f2f10cdf354270ac97c1f091d0846e8154749b4b8347f5f26a40184d425
```

The executing llama.cpp launcher was verified from `/proc/<pid>/exe`; the loaded `libllama-server-impl.so` was verified from `/proc/<pid>/maps`.

## External Kaggle inputs

```text
Qwen3-Embedding-4B=dangkhoa2016/qwen-qwen3-embedding-4b
Qwen3-Reranker-4B GGUF=dangkhoa2016/giladgd-qwen3-reranker-4b-gguf
Qdrant snapshot=dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k
Qwen3-Reranker-4B hardened runtime=dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime
```

Changes that alter qualified behavior require fresh qualification evidence.
