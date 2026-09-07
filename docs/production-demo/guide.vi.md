# Hướng dẫn chạy Kaggle production demo
> 🌐 Language / Ngôn ngữ: [English](guide.md) | **Tiếng Việt**

1. Attach `dangkhoa2016/qwen-qwen3-embedding-4b` → Transformers / `default` / Version `1`.
2. Attach `dangkhoa2016/giladgd-qwen3-reranker-4b-gguf` chứa `Qwen3-Reranker-4B.Q4_K_M.gguf`.
3. Attach `dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k` chứa `knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot`.
4. Attach `dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime`.
5. Đặt `Accelerator: None (CPU)` và `Internet: On`.
6. Mở `notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb`.
7. Dùng **Restart Session → Run All**.

Không seed hoặc re-embed collection 20K. Notebook restore immutable canonical snapshot.

Qualified configuration:

```text
RETRIEVAL_TOP_K=5
RERANK_TOP_K=5
DISPLAY_TOP_K=5
LLAMA_SERVER_THREADS=2
TORCH_NUM_THREADS=2
```

Publication-ready qualification reference pass 3/3 semantic cases, zero cgroup OOM/OOM-kill, qualified pipeline `468.489s`, notebook total `469.782s`, trong threshold `600s`.

Xem `qualification.vi.md` và `provenance.vi.md`.

## Run All lặp lại an toàn

Lần **Run All** thứ hai trong cùng session trước tiên thực hiện verified-owned cleanup. Process chưa được xác minh trên các port `6333`, `8000` hoặc `8081` không bao giờ bị terminate tự động.
