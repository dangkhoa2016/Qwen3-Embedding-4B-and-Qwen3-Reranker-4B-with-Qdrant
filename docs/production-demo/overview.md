# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant - Production Demo
> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](overview.vi.md)

This production demo exercises the qualified retrieval path:

```text
query
  -> Qwen3-Embedding-4B (Transformers CPU FP16)
  -> Qdrant 1.18.3 / canonical 20K bilingual collection
  -> Top-5 candidates
  -> Qwen3-Reranker-4B Q4_K_M (qualified hardened llama.cpp runtime)
  -> final ranked results
```

## Qualified configuration

```text
RETRIEVAL_TOP_K=5
RERANK_TOP_K=5
DISPLAY_TOP_K=5
LLAMA_SERVER_THREADS=2
TORCH_NUM_THREADS=2
```

Fresh Kaggle qualification passed 3/3 semantic cases, recorded zero cgroup OOM/OOM-kill events, completed the qualified pipeline in `468.489s`, and completed the notebook in `469.782s` within the `600s` threshold.

## Required Kaggle inputs

1. `dangkhoa2016/qwen-qwen3-embedding-4b`
2. `dangkhoa2016/giladgd-qwen3-reranker-4b-gguf` with `Qwen3-Reranker-4B.Q4_K_M.gguf`
3. `dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k` with `knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot`
4. `dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime` with `RUNTIME-MANIFEST.sha256` and the complete eight-file hardened runtime bundle

Kaggle mounts datasets under `/kaggle/input/datasets/<owner>/<slug>` and models under `/kaggle/input/models/<owner>/<slug>/...`. The notebook checks the exact canonical runtime path first and uses a fail-closed recursive lookup only inside `/kaggle/input/datasets` if necessary.

Snapshot identity:

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

Open `notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb`, attach all four inputs, choose CPU (`Accelerator: None`) with Internet On, then use **Restart Session → Run All**.

## Reproducibility pins

- Qdrant: `1.18.3`
- Qwen3-Reranker-4B GGUF: `Q4_K_M`
- llama.cpp pin: `b10699`
- Qdrant collection: `knowledge_entities_qwen3_4b_text_v21`
- Retrieval default: `K=5`

See [Production qualification](qualification.md) and [Provenance](provenance.md).

## Safe repeated Run All

Before starting services, the notebook checks for state from a prior run in the same Kaggle session. It terminates only processes whose ownership is proven from PID/`/proc` evidence, process identity, expected ports, working directory or storage path, and the frozen Qwen3-Reranker-4B launcher identity. If a required port is held by an unverified process, the notebook fails closed and does not kill it.
