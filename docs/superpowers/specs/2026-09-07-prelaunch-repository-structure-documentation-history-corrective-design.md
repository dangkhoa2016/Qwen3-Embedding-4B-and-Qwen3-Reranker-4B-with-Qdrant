# Prelaunch Repository Structure, Documentation, Identity, and History Corrective Design

**Date:** 2026-09-07  
**Repository:** `dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant`  
**Status:** Approved design, awaiting implementation-plan review  
**Scope:** Pre-publication corrective before fresh Kaggle evidence and social launch

## 1. Purpose

The repository has already proven runtime, package, CI, tag, and release integrity, but its current public structure and history are not yet publication-quality. This corrective reorganizes the repository without changing the qualified retrieval semantics.

The work addresses four repository-quality problems plus two newly locked requirements:

1. The retired distribution identity `qwen3-embedding-4b-reranker-4b-qdrant` is still spread through the current tree.
2. The current tip commit mixes unrelated responsibilities across a very large number of files.
3. `README.md` and `README.vi.md` are too shallow as public landing pages and do not provide proper Markdown navigation to the project documentation.
4. Public Markdown files are poorly organized, with too many top-level files and too little use of `docs/`.
5. All historical commit messages need modern, diff-grounded subjects plus bullet bodies.
6. Official GitHub Actions should use readable current major tags such as `@v7`, not raw commit SHA pins.

This corrective is intentionally completed before any fresh Kaggle publication proof.

## 2. Non-goals and frozen semantic boundary

This corrective MUST NOT intentionally change the qualified production behavior.

The following production facts remain frozen unless implementation work proves an unavoidable semantic impact and explicitly reopens qualification:

```text
Retrieval default: K=5
Qdrant version: 1.18.3
Collection: knowledge_entities_qwen3_4b_text_v21
Points: 20000
Vector size: 2560
Distance: cosine
Snapshot: knowledge_entities_qwen3_4b_text_v21-20260827T013824Z.snapshot
Snapshot size: 283812352
Snapshot SHA256: 71f12fe14ef51966069347290ad15302d389e488d7904dab6cf0cf190f43064f
Reranker GGUF: Qwen3-Reranker-4B.Q4_K_M.gguf
Reranker GGUF SHA256: 941f7d1d1524251c026a797b803ac9575545c5d7aa19b26e0e49661d7720af49
llama.cpp pin: b10699
Qualified pipeline: 468.489s
Verified Run All: 469.782s
Qualification threshold: 600s
Semantic validation: 3/3 PASS
cgroup OOM delta: 0
cgroup OOM-kill delta: 0
```

The namespace migration is allowed to change import paths, packaging paths, tests, documentation, and automation, but the runtime behavior behind those imports must remain equivalent.

## 3. Canonical identity contract

### 3.1 Public display identity

The human-readable project name is exactly:

```text
Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant
```

Use this value in prose, headings, README titles, documentation, release-note prose, and runtime display metadata.

### 3.2 Canonical machine slug

When spaces cannot be used and case is acceptable:

```text
Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant
```

This is also the canonical GitHub repository slug.

### 3.3 Lowercase machine slug and Python distribution

Use:

```text
qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant
```

This is the canonical Python distribution name and the preferred lowercase machine-readable slug.

### 3.4 Python normalized stem and import namespace

Use:

```text
qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant
```

The source package becomes:

```text
src/qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant/
```

The built distribution filenames therefore follow normal Python normalization, for example:

```text
qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant-1.0.0-py3-none-any.whl
qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant-1.0.0.tar.gz
```

### 3.5 Runtime metadata

Runtime metadata should clearly distinguish project name, slug, distribution, and version. A target shape is:

```python
__version__ = "1.0.0"
__project_name__ = "Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant"
__project_slug__ = "Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant"
__distribution_name__ = "qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant"
```

### 3.6 Retired current-tree identities

The following strings are retired and MUST be absent from the current public tree except inside explicit tests that construct them in fragments solely to prove their absence:

```text
qwen3-embedding-4b-reranker-4b-qdrant
qwen3_embedding_4b_reranker_4b_qdrant
qwen3_qdrant
```

Historical Git objects may naturally contain old values, but the reconstructed public history should avoid preserving obsolete public identities when those commits are being editorially rewritten.

## 4. Release identity contract

The Git tag remains:

```text
v1.0.0
```

The GitHub Release title MUST be exactly:

```text
v1.0.0
```

The English release-note H1 MUST be:

```markdown
# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant - v1.0.0
```

The Vietnamese release-note H1 must use the same canonical project identity and `v1.0.0`.

The GitHub Release body should be sourced from the canonical release note rather than independently drifting from it.

The project is not being published to PyPI in this release. Public documentation should not present PyPI as an active release channel.

## 5. Repository documentation topology

The repository root should remain small and navigable. The target public topology is:

```text
.
├── README.md
├── README.vi.md
├── LICENSE
├── pyproject.toml
├── MANIFEST.in
├── MANIFEST.sha256
├── requirements*.txt
├── .env.example
│
├── .github/
│   ├── CODEOWNERS
│   ├── CONTRIBUTING.md
│   ├── CONTRIBUTING.vi.md
│   ├── SECURITY.md
│   ├── SECURITY.vi.md
│   ├── CODE_OF_CONDUCT.md
│   ├── CODE_OF_CONDUCT.vi.md
│   ├── SUPPORT.md
│   ├── SUPPORT.vi.md
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── PULL_REQUEST_TEMPLATE.vi.md
│   └── workflows/
│
├── docs/
│   ├── README.md
│   ├── README.vi.md
│   ├── production-demo/
│   │   ├── overview.md
│   │   ├── overview.vi.md
│   │   ├── guide.md
│   │   ├── guide.vi.md
│   │   ├── qualification.md
│   │   ├── qualification.vi.md
│   │   ├── provenance.md
│   │   ├── provenance.vi.md
│   │   ├── roadmap.md
│   │   └── roadmap.vi.md
│   └── releases/
│       ├── v1.0.0.md
│       └── v1.0.0.vi.md
│
├── notebooks/
├── corpus/
├── examples/
├── scripts/
├── src/
├── tests/
└── tools/
```

Root-level project README files remain root because GitHub uses them as repository landing pages. Community health files are moved under `.github/`, where GitHub understands them natively. Detailed product, reproduction, qualification, provenance, roadmap, and release documentation moves under `docs/`.

## 6. README requirements

Both root README files must be full project landing pages rather than short summaries.

They should contain synchronized sections for:

- project overview and purpose;
- architecture;
- feature/capability summary;
- production qualification summary;
- requirements and external inputs;
- installation;
- quick start;
- API overview with representative examples;
- Qdrant production demo;
- reproducibility and provenance;
- documentation index;
- testing and development;
- security;
- contributing;
- known limitations;
- release information;
- license.

All local documentation references must be proper Markdown links, not backtick-only filenames.

The English and Vietnamese README files must preserve technical parity. Commands, hashes, filenames, URLs, runtime defaults, and qualification results should be byte-for-byte equivalent where language does not require translation.

## 7. Documentation navigation contract

`docs/README.md` and `docs/README.vi.md` become documentation indexes.

Every bilingual documentation pair must link to its counterpart. The root README files must link to the documentation indexes and all high-value operator documentation.

The corrective must include an automated local-link checker that validates:

- every relative Markdown link resolves;
- anchors used by repository documentation resolve where practical;
- bilingual counterpart files exist;
- no root README navigation points to retired paths;
- release notes and production-demo documents link to canonical relocated paths.

## 8. GitHub Actions policy

Official GitHub Actions should use readable current supported major tags instead of raw commit SHA pins.

At design time, the verified current major lines are:

```yaml
uses: actions/checkout@v7
uses: actions/setup-python@v7
uses: actions/upload-artifact@v7
```

The implementation must re-check upstream releases immediately before finalizing the corrective. If a newer stable major is current and compatible, use that newer supported major; otherwise use `v7`.

The workflow must reject raw 40-character SHA references for `actions/*` dependencies under the repository policy.

The CI workflow should avoid hard-coded distribution filenames where metadata can be derived from `pyproject.toml`. Package verification should discover the produced wheel/sdist and assert their metadata rather than duplicating long normalized names in many places.

## 9. Git history reconstruction

### 9.1 Objective

The public `v1.0.0` history should read as a coherent technical narrative. The previous constraint that early commit SHAs must remain unchanged is removed.

All public-history commit SHAs may change because commit messages are being amended from the root commit onward.

### 9.2 Metadata preservation

Where an existing logical commit boundary is retained, preserve:

```text
Author: Đăng Khoa <i.am@dangkhoa.dev>
Committer: Đăng Khoa <i.am@dangkhoa.dev>
AuthorDate: original timestamp
CommitterDate: original timestamp
```

When one mixed commit is split into multiple logical commits, new timestamps must remain chronologically valid and close to the original development period. The final reconstructed history must remain strictly readable in chronological order.

### 9.3 Commit-message format

Every retained or reconstructed public commit should use:

```text
<type>(<optional-scope>): <concise subject>

- <diff-grounded responsibility or behavior>
- <specific implementation, contract, or compatibility detail>
- <verification, qualification, or integration consequence when applicable>
```

Allowed primary types:

```text
feat
refactor
test
docs
ci
build
chore
```

Bodies must be grounded in the actual diff associated with the reconstructed commit. Do not add claims that were not true at that point in the history. Do not use generic filler bullets.

### 9.4 Mega-commit decomposition

The current tip commit `cf831e90f9e762033b914ba66906fbc710f36bb8` must not survive as one mixed-responsibility commit.

Its content should be redistributed into single-responsibility historical commits, especially around:

- production-demo qualification and notebook evidence;
- v1.0.0 packaging;
- canonical identity migration;
- bilingual documentation and repository organization;
- CI/release hardening and publication guards.

The final commit count is not fixed. Quality and logical boundaries take precedence over preserving the old count.

## 10. Test-driven corrective gates

Before moving `main`, the reconstructed branch must pass automated gates covering at least:

```text
CANONICAL_DISPLAY_NAME=PASS
CANONICAL_REPOSITORY_SLUG=PASS
CANONICAL_LOWERCASE_SLUG=PASS
CANONICAL_PYTHON_NAMESPACE=PASS
RETIRED_DISTRIBUTION_NAME_ABSENT=PASS
RETIRED_WHEEL_STEM_ABSENT=PASS
RETIRED_IMPORT_NAMESPACE_ABSENT=PASS
ROOT_MARKDOWN_LAYOUT=PASS
DOCS_INDEX=PASS
RELATIVE_MARKDOWN_LINKS=PASS
BILINGUAL_PAIR_COMPLETENESS=PASS
README_NAVIGATION=PASS
GITHUB_ACTIONS_AUDIT=PASS
RAW_COMMIT_SHA_ACTION_PINS=0
DEPRECATED_ACTION_MAJORS=0
COMMIT_MESSAGE_FORMAT=PASS
COMMIT_SUBJECT_QUALITY=PASS
COMMIT_BODY_BULLETS=PASS
COMMIT_BODY_DIFF_GROUNDED=PASS
NO_GENERIC_COMMIT_BODIES=PASS
NO_MIXED_RESPONSIBILITY_MEGA_COMMIT=PASS
AUTHOR_IDENTITY=PASS
CHRONOLOGY=PASS
FULL_REGRESSION=PASS
PACKAGE_BUILD=PASS
PACKAGE_METADATA=PASS
SOURCE_MANIFEST=PASS
PUBLICATION_NOTEBOOK_VALIDATION=PASS
```

Existing semantic regression tests must continue to pass after the namespace migration.

## 11. Packaging and manifest changes

`pyproject.toml` must adopt the new distribution identity and package discovery path.

`MANIFEST.in` must follow the relocated community/documentation files. Package-content checks must be updated to verify the new paths deliberately included in the sdist.

`MANIFEST.sha256` must be regenerated only after the final reconstructed tree is complete.

Deterministic build behavior using `SOURCE_DATE_EPOCH` should be retained.

## 12. Publication sequence

No destructive publication update occurs until the reconstructed branch passes all local and CI-equivalent gates.

The final sequence is:

```text
1. Freeze and audit current live state.
2. Build the complete reconstructed history on an isolated branch/worktree.
3. Run history-quality, source, docs, package, and semantic verification.
4. Verify the final tree contains no retired identity or broken links.
5. Temporarily disable the main ruleset only for the controlled rewrite window.
6. Force-update main with explicit lease/precondition checks.
7. Restore the main ruleset immediately.
8. Require main CI success.
9. Recreate annotated v1.0.0 only after main CI passes.
10. Require tag CI success.
11. Use only the new tag CI artifact as the canonical release distribution source.
12. Replace GitHub Release assets.
13. Set GitHub Release title exactly to v1.0.0.
14. Set the GitHub Release body from the canonical v1.0.0 release note.
15. Keep immutable releases disabled unless separately approved.
16. Do not create tag protection unless separately approved.
17. Produce and audit a final forensic evidence bundle.
```

## 13. Failure and rollback policy

The corrective is fail-closed.

Before the main rewrite, capture:

- current main commit and tree;
- current annotated tag object and target;
- current release metadata and all release asset digests;
- current ruleset JSON;
- current CI IDs and artifact IDs.

If any step fails after a destructive publication mutation, restore the previously captured public state before retrying unless the failed step can be safely resumed without ambiguity.

Never declare acceptance from a partial state.

## 14. Security/process note

This corrective does not reopen the previously documented decision about the old GitHub PAT. The implementation must not print or archive credential plaintext. Final evidence must be scanned for secret-like tokens and credential-bearing remote URLs.

## 15. Acceptance and next phase

The corrective is accepted only when repository structure, identity, documentation, history, CI, package artifacts, tag, release, and forensic evidence all agree.

Final acceptance should permit:

```text
PRELAUNCH_REPOSITORY_CORRECTIVE=ACCEPTED
PUBLICATION_READY=YES
NEXT=FRESH_KAGGLE_PRODUCTION_DEMO_AND_PUBLIC_NOTEBOOK_EVIDENCE
```

Fresh Kaggle execution remains blocked until this corrective is accepted.
