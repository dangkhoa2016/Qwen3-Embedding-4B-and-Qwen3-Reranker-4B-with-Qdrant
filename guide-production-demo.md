# Kaggle production-demo execution guide
> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](guide-production-demo.vi.md)

1. Attach `dangkhoa2016/qwen-qwen3-embedding-4b` → Transformers / `default` / Version `1`.
2. Attach `dangkhoa2016/giladgd-qwen3-reranker-4b-gguf` containing `Qwen3-Reranker-4B.Q4_K_M.gguf`.
3. Attach `dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k` containing `knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot`.
4. Attach `dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime`.
5. Set `Accelerator: None (CPU)` and `Internet: On`.
6. Open `notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb`.
7. Use **Restart Session → Run All**.

Do not seed or re-embed the 20K collection. The notebook restores the immutable canonical snapshot.

Qualified configuration:

```text
RETRIEVAL_TOP_K=5
RERANK_TOP_K=5
DISPLAY_TOP_K=5
LLAMA_SERVER_THREADS=2
TORCH_NUM_THREADS=2
```

The publication-ready qualification reference passed 3/3 semantic cases, recorded zero cgroup OOM/OOM-kill events, completed the qualified pipeline in `468.489s`, and completed the notebook in `469.782s` within the `600s` threshold.

See `PRODUCTION_QUALIFICATION.md` and `PRODUCTION_DEMO_PROVENANCE.md`.

## Safe repeated Run All

A second **Run All** in the same session first performs verified-owned cleanup. Unverified processes on ports `6333`, `8000`, or `8081` are never terminated automatically.
