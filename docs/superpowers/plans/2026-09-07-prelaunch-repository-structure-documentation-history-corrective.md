# Prelaunch Repository Structure, Documentation, Identity, and History Corrective Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconstruct the pre-publication repository and Git history so the v1.0.0 public state uses one canonical identity, a navigable bilingual documentation hierarchy, readable current-major GitHub Actions, focused commits with modern bullet bodies, and release artifacts that match the reconstructed tag.

**Architecture:** Perform all source and history work in an isolated real Git checkout/worktree. Add fail-closed tests first, migrate the Python distribution/import namespace, reorganize and rewrite documentation, modernize CI/package validation, regenerate the source manifest, then reconstruct Git history with `git commit-tree`/rebase plumbing so author/committer identity and dates are explicitly controlled. Only after the reconstructed branch passes all gates may the executor temporarily relax the main ruleset, update `main`, recreate `v1.0.0`, replace release assets, and produce forensic evidence.

**Tech Stack:** Git, Python 3.10/3.12, pytest, setuptools/build, GitHub Actions, GitHub REST/`gh`, Markdown, Kaggle notebook JSON.

**Spec:** `docs/superpowers/specs/2026-09-07-prelaunch-repository-structure-documentation-history-corrective-design.md`

## Global Constraints

- Display name: `Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant`.
- Canonical repository slug: `Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant`.
- Lowercase/distribution slug: `qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant`.
- Python normalized stem/import namespace: `qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant`.
- Retired current-tree identities: `qwen3-embedding-4b-reranker-4b-qdrant`, `qwen3_embedding_4b_reranker_4b_qdrant`, `qwen3_qdrant`.
- Release tag: `v1.0.0`.
- GitHub Release title: exactly `v1.0.0`.
- Release-note H1: `# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant - v1.0.0`.
- No PyPI publication claim for v1.0.0.
- Official GitHub Actions use current supported major tags; verified design baseline is `actions/checkout@v7`, `actions/setup-python@v7`, `actions/upload-artifact@v7`.
- Author and committer identity: `Đăng Khoa <i.am@dangkhoa.dev>`.
- Preserve original author/committer timestamps for retained logical commit boundaries; assign chronologically valid nearby timestamps only to newly split boundaries.
- Preserve K=5, Qdrant 1.18.3, canonical 20K snapshot, GGUF/runtime hashes, 468.489s qualified pipeline, 469.782s Run All, 600s gate, semantic 3/3 PASS, OOM/OOM-kill delta 0.
- Do not update `main`, `v1.0.0`, rulesets, or GitHub Release until the reconstructed candidate passes all pre-publication gates.

---

### Task 1: Isolated Worktree, Baseline Freeze, and Corrective Harness

**Files:**
- Create: `tools/prelaunch_corrective/common.py`
- Create: `tools/prelaunch_corrective/freeze_state.py`
- Create: `tests/test_prelaunch_corrective_tools.py`
- Evidence output: `.prelaunch-corrective/baseline/` (ignored, never committed)

**Interfaces:**
- Produces `tools.prelaunch_corrective.common.run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]`.
- Produces `freeze_state.py --repo OWNER/REPO --out DIR`, which writes `git-state.json`, `ruleset.json`, `tag-ref.json`, `tag-object.json`, `release.json`, `main-ci.json`, and `tag-ci.json` without credential plaintext.

- [ ] **Step 1: Create the isolated checkout before editing**

Run under the executor host after invoking `superpowers:using-git-worktrees`:

```bash
git fetch --all --tags --prune
git worktree add ../qwen3-prelaunch-corrective -b prelaunch-repository-corrective main
cd ../qwen3-prelaunch-corrective
git status --short --branch
```

Expected: clean branch based exactly on the live `main` precondition SHA.

- [ ] **Step 2: Write the failing corrective-tool test**

```python
from pathlib import Path
from tools.prelaunch_corrective.common import redact_url


def test_redact_url_removes_embedded_credentials():
    assert redact_url("https://token@example.invalid/o/r.git") == "https://example.invalid/o/r.git"
```

Run:

```bash
PYTHONPATH=. pytest -q tests/test_prelaunch_corrective_tools.py
```

Expected: FAIL because `tools/prelaunch_corrective/common.py` does not exist.

- [ ] **Step 3: Implement the minimal safe command/redaction helpers**

`redact_url()` must remove userinfo before `@`; `run()` must use argument arrays, `text=True`, `check=True`, and never echo environment variables containing `TOKEN`, `PASSWORD`, or `SECRET`.

- [ ] **Step 4: Implement and run baseline freeze**

Capture at minimum:

```text
main SHA/tree
15-commit current history with author/committer dates
ruleset 22445904
annotated v1.0.0 tag ref/object/target
GitHub Release 384014172 metadata and five asset digests
main CI 34129363649
tag CI 34129375908
Actions artifact 10021464918
```

Run:

```bash
python tools/prelaunch_corrective/freeze_state.py \
  --repo dangkhoa2016/Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant \
  --out .prelaunch-corrective/baseline
```

Expected: all JSON files written; grep for credential-like URL userinfo returns no match.

- [ ] **Step 5: Commit the harness**

```text
chore(corrective): add fail-closed prelaunch state capture

- Capture repository, ruleset, tag, release, CI, and artifact preconditions before destructive work.
- Redact credential-bearing URLs and avoid persisting token-bearing environment values.
- Keep generated baseline evidence outside the tracked source tree.
```

---

### Task 2: Lock Canonical Identity and Namespace With Failing Tests

**Files:**
- Modify: `tests/test_release_identity.py`
- Modify: `tests/test_public_repository_hygiene.py`
- Create: `tests/test_canonical_identity_contract.py`

**Interfaces:**
- Tests expose exact constants `DISPLAY_NAME`, `CANONICAL_SLUG`, `DIST_NAME`, and `IMPORT_NAME` in `tests/test_canonical_identity_contract.py` so later tasks import one contract instead of duplicating strings.

- [ ] **Step 1: Add exact failing assertions**

```python
DISPLAY_NAME = "Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant"
CANONICAL_SLUG = "Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant"
DIST_NAME = "qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant"
IMPORT_NAME = "qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant"
RETIRED = (
    "qwen3-embedding-4b-reranker-4b-qdrant",
    "qwen3_embedding_4b_reranker_4b_qdrant",
    "qwen3_qdrant",
)
```

Tests must assert:

```text
pyproject project.name == DIST_NAME
src/<IMPORT_NAME>/__init__.py exists
src/qwen3_qdrant does not exist
__project_name__ == DISPLAY_NAME
__project_slug__ == CANONICAL_SLUG
__distribution_name__ == DIST_NAME
all retired current-tree identities absent outside fragmented negative tests
```

Run:

```bash
PYTHONPATH=src:. pytest -q tests/test_canonical_identity_contract.py tests/test_release_identity.py
```

Expected: FAIL on current distribution and `src/qwen3_qdrant`.

- [ ] **Step 2: Update old hygiene assertions to the new contract**

Replace old package-name, source-path, and CI SHA-pin expectations. Tests must build retired strings from fragments in negative tests so the literal retired values do not remain in tracked current-tree text.

- [ ] **Step 3: Keep tests failing and commit nothing yet**

This task intentionally ends as the RED half consumed immediately by Task 3; no standalone failing-test commit is pushed to the reconstructed public history.

---

### Task 3: Migrate Distribution and Python Import Namespace

**Files:**
- Rename directory: `src/qwen3_qdrant/` → `src/qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant/`
- Modify: `pyproject.toml`
- Modify: every Python/shell/notebook import or package-path reference returned by `git grep -n 'qwen3_qdrant\|qwen3-embedding-4b-reranker-4b-qdrant\|qwen3_embedding_4b_reranker_4b_qdrant'`
- Modify: relevant tests under `tests/`

**Interfaces:**
- Runtime package exports:

```python
__version__ = "1.0.0"
__project_name__ = "Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant"
__project_slug__ = "Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant"
__distribution_name__ = "qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant"
```

- [ ] **Step 1: Rename the package with Git-aware moves**

```bash
git mv src/qwen3_qdrant src/qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant
```

- [ ] **Step 2: Update package metadata**

Set `[project].name` to `qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant`; retain version `1.0.0`, author, license, Python floor, dependencies, and canonical repository URLs.

- [ ] **Step 3: Update imports and module paths without changing behavior**

Use `git grep` to enumerate references first, update only names/paths, and do not alter model loading, K=5, Qdrant, GGUF, concurrency, authentication, instruction, or timing semantics.

- [ ] **Step 4: Run namespace and semantic regression gates**

```bash
PYTHONPATH=src:. pytest -q tests/test_canonical_identity_contract.py tests/test_release_identity.py
PYTHONPATH=src pytest -q tests/test_api.py tests/test_engine_contracts.py tests/test_production_demo.py tests/test_gguf_reranker_engine.py
python -m compileall -q src scripts tools tests
```

Expected: PASS.

- [ ] **Step 5: Commit**

```text
refactor(identity): adopt the canonical project and package identity

- Rename the Python distribution and import namespace to the full Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant identity.
- Distinguish display name, repository slug, distribution name, and runtime version metadata explicitly.
- Preserve qualified embedding, reranking, Qdrant, authentication, and production-demo behavior across the namespace migration.
```

---

### Task 4: Reorganize Community and Product Documentation

**Files:**
- Move: `CONTRIBUTING.md` → `.github/CONTRIBUTING.md`
- Move: `CONTRIBUTING.vi.md` → `.github/CONTRIBUTING.vi.md`
- Move: `SECURITY.md` → `.github/SECURITY.md`
- Move: `SECURITY.vi.md` → `.github/SECURITY.vi.md`
- Move: `README_PRODUCTION_DEMO.md` → `docs/production-demo/overview.md`
- Move: `README_PRODUCTION_DEMO.vi.md` → `docs/production-demo/overview.vi.md`
- Move: `guide-production-demo.md` → `docs/production-demo/guide.md`
- Move: `guide-production-demo.vi.md` → `docs/production-demo/guide.vi.md`
- Move: `PRODUCTION_QUALIFICATION.md` → `docs/production-demo/qualification.md`
- Move: `PRODUCTION_QUALIFICATION.vi.md` → `docs/production-demo/qualification.vi.md`
- Move: `PRODUCTION_DEMO_PROVENANCE.md` → `docs/production-demo/provenance.md`
- Move: `PRODUCTION_DEMO_PROVENANCE.vi.md` → `docs/production-demo/provenance.vi.md`
- Move: `RELEASE_NOTES_v1.0.0.md` → `docs/releases/v1.0.0.md`
- Move: `RELEASE_NOTES_v1.0.0.vi.md` → `docs/releases/v1.0.0.vi.md`
- Create: `docs/README.md`
- Create: `docs/README.vi.md`
- Create: `tests/test_documentation_topology.py`
- Create: `tests/test_markdown_links.py`

**Interfaces:**
- `tests/test_markdown_links.py` provides `iter_markdown_links(path: Path) -> Iterable[str]` and validates relative file targets from repository root semantics.

- [ ] **Step 1: Write topology/link tests against target paths**

Assert root product docs are absent, target docs exist, every English `.md` has a `.vi.md` peer except explicitly non-bilingual machine/community exceptions, and relative Markdown links resolve.

Run:

```bash
pytest -q tests/test_documentation_topology.py tests/test_markdown_links.py
```

Expected: FAIL before moves.

- [ ] **Step 2: Move files with `git mv` and create documentation indexes**

`docs/README.md` must link to production overview, guide, qualification, provenance, roadmap, release v1.0.0, security, and contributing. `docs/README.vi.md` must mirror the same topology.

- [ ] **Step 3: Update every moved relative link**

Run:

```bash
git grep -nE 'README_PRODUCTION_DEMO|guide-production-demo|PRODUCTION_QUALIFICATION|PRODUCTION_DEMO_PROVENANCE|RELEASE_NOTES_v1\.0\.0|\bSECURITY\.md|\bCONTRIBUTING\.md'
```

Only intentionally historical references in non-public evidence may remain; current tracked navigation must point to new paths.

- [ ] **Step 4: Run topology/link tests**

```bash
pytest -q tests/test_documentation_topology.py tests/test_markdown_links.py tests/test_public_repository_hygiene.py
```

Expected: PASS after Task 5 completes README content; topology/link subset must PASS now.

- [ ] **Step 5: Commit**

```text
docs: organize bilingual project documentation

- Move community-health files under .github and production/release documentation under a structured docs hierarchy.
- Add English and Vietnamese documentation indexes with direct navigation to operator and release material.
- Preserve qualification, provenance, roadmap, security, and contributing content while replacing retired root paths.
```

---

### Task 5: Rewrite the English and Vietnamese README Landing Pages

**Files:**
- Modify: `README.md`
- Modify: `README.vi.md`
- Modify: `docs/production-demo/overview*.md`
- Modify: `docs/releases/v1.0.0*.md`
- Modify: `tests/test_public_repository_hygiene.py`
- Modify: `tests/test_documentation_topology.py`

**Interfaces:**
- Root README pair is the canonical landing-page summary; detailed facts link to `docs/` rather than duplicating large operational documents.

- [ ] **Step 1: Add failing README section/navigation assertions**

Require both languages to cover equivalent sections for overview, architecture, capabilities, qualification, requirements/external inputs, installation, quick start, API, production demo, reproducibility/provenance, documentation index, testing, security, contributing, limitations, release, and license.

Require clickable Markdown links to:

```text
docs/README.md or docs/README.vi.md
docs/production-demo/overview*.md
docs/production-demo/guide*.md
docs/production-demo/qualification*.md
docs/production-demo/provenance*.md
docs/releases/v1.0.0*.md
.github/SECURITY*.md
.github/CONTRIBUTING*.md
```

- [ ] **Step 2: Rewrite `README.md`**

Keep exact qualified facts, four external Kaggle inputs, K=5/Qdrant contract, representative start command, endpoint overview, and prominent documentation links. Avoid package-slug prose unless discussing installation/package metadata.

- [ ] **Step 3: Rewrite `README.vi.md` for technical parity**

Ensure the Vietnamese README includes every operational command present in English, including `set -a`, `source .env`, `set +a`, and `bash scripts/start-server.sh` when used.

- [ ] **Step 4: Normalize production/release headings**

Set production overview to the canonical display name; set release-note H1 exactly:

```markdown
# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant - v1.0.0
```

Remove any active PyPI-publication wording.

- [ ] **Step 5: Run README/docs gates**

```bash
pytest -q tests/test_documentation_topology.py tests/test_markdown_links.py tests/test_public_repository_hygiene.py
```

Expected: PASS.

- [ ] **Step 6: Commit**

```text
docs(readme): build complete bilingual project landing pages

- Expand both README files with architecture, setup, API, production proof, reproducibility, limitations, and release guidance.
- Link every high-value operator and contributor document through the new docs and .github hierarchy.
- Keep English and Vietnamese commands, hashes, model identities, and qualification results technically synchronized.
```

---

### Task 6: Modernize GitHub Actions and Centralize Package Verification

**Files:**
- Modify: `.github/workflows/ci.yml`
- Create: `scripts/verify_distribution.py`
- Create: `tests/test_ci_policy.py`
- Create: `tests/test_distribution_verifier.py`
- Modify: `tests/test_public_repository_hygiene.py`

**Interfaces:**
- `scripts/verify_distribution.py --dist-dir dist` reads `pyproject.toml`, discovers exactly one wheel and one sdist, validates metadata/version/license/package namespace, and exits nonzero on mismatch.

- [ ] **Step 1: Verify upstream official Action major lines immediately before edit**

Use GitHub Releases API for `actions/checkout`, `actions/setup-python`, `actions/upload-artifact`. At the approved design baseline all are on major `v7`; use a newer stable major only if upstream has actually advanced and compatibility is validated.

- [ ] **Step 2: Write failing CI policy tests**

Assert workflow contains readable major tags, contains no `actions/*@[0-9a-f]{40}`, has Python 3.10/3.12 matrix, full pytest, manifest validation, publication-notebook validation, deterministic build, and tag-only artifact upload.

- [ ] **Step 3: Replace raw SHA pins**

Target baseline:

```yaml
uses: actions/checkout@v7
uses: actions/setup-python@v7
uses: actions/upload-artifact@v7
```

- [ ] **Step 4: Move package verification out of large inline YAML**

CI should run:

```bash
python scripts/verify_distribution.py --dist-dir dist
```

The verifier derives project name/version from `pyproject.toml`, discovers outputs, and asserts package directory `qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant/` exists in wheel/sdist without repeating the old stem throughout YAML.

- [ ] **Step 5: Use canonical artifact naming**

Use:

```yaml
name: qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant-${{ github.ref_name }}-dist
```

- [ ] **Step 6: Run tests**

```bash
pytest -q tests/test_ci_policy.py tests/test_distribution_verifier.py tests/test_public_repository_hygiene.py
```

Expected: PASS.

- [ ] **Step 7: Commit**

```text
ci(release): modernize GitHub Actions and package validation

- Use current supported major tags for official checkout, Python setup, and artifact upload actions.
- Centralize wheel and sdist verification so CI derives canonical distribution metadata instead of duplicating filenames.
- Retain full regression, manifest, notebook, deterministic-build, and tag-only release artifact gates.
```

---

### Task 7: Update Notebook, Scripts, Manifests, and Packaging for Relocated Paths

**Files:**
- Modify: `notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb`
- Modify: `scripts/validate-publication-notebook.py`
- Modify: `scripts/check-canonical-model-naming.py`
- Modify: `MANIFEST.in`
- Modify: package/source path references under `scripts/`, `tools/`, `tests/`
- Modify: `tests/test_publication_ready_kaggle_notebook.py`
- Modify: `tests/test_publication_hygiene.py`

**Interfaces:**
- Naming guard must fail on literal retired identities and accept canonical display/slug/import identities in their proper contexts.

- [ ] **Step 1: Add failing notebook/naming assertions for new identities and docs paths**

Keep production semantics unchanged; only identity/import/document references are permitted to change.

- [ ] **Step 2: Update notebook JSON deterministically**

Use a Python JSON transform rather than manual formatting. Preserve cell order, production commands, K=5, external inputs, runtime hashes, and evidence gates.

- [ ] **Step 3: Update `MANIFEST.in`**

Explicitly include intended `.github/SECURITY*`, `.github/CONTRIBUTING*`, `README.vi.md`, `LICENSE`, and documentation required in the sdist. Do not include temporary corrective evidence.

- [ ] **Step 4: Run publication notebook and operator tests**

```bash
python scripts/check-canonical-model-naming.py .
python scripts/validate-publication-notebook.py notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb
pytest -q tests/test_publication_ready_kaggle_notebook.py tests/test_publication_hygiene.py tests/test_production_demo_operator_files.py
```

Expected: PASS.

- [ ] **Step 5: Commit**

```text
test(publication): align notebook and publication guards with the canonical layout

- Update publication-ready notebook and validation references for the canonical namespace and documentation paths.
- Strengthen naming guards so retired package and import identities cannot re-enter the current public tree.
- Preserve the qualified K=5 production workflow, external-input identities, and runtime evidence contracts.
```

---

### Task 8: Regenerate Source Manifest and Prove Final Candidate Tree

**Files:**
- Modify: `MANIFEST.sha256`
- Generated: `dist/` (not committed)
- Generated: `.prelaunch-corrective/candidate/` (not committed)

**Interfaces:**
- Candidate evidence records exact tree SHA, tests, build hashes, retired-token scan, link scan, and semantic-file diff classification.

- [ ] **Step 1: Run the complete suite before regenerating manifest**

```bash
PYTHONPATH=src pytest -q
python -m compileall -q src scripts tools tests
while IFS= read -r -d '' f; do bash -n "$f"; done < <(find scripts tools -type f -name '*.sh' -print0)
python scripts/check-canonical-model-naming.py .
python scripts/validate-publication-notebook.py notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb
```

Expected: PASS.

- [ ] **Step 2: Regenerate manifest from tracked files**

```bash
git ls-files -z | while IFS= read -r -d '' path; do
  [ "$path" = MANIFEST.sha256 ] && continue
  sha256sum "$path"
done | LC_ALL=C sort -k2 > MANIFEST.sha256
sha256sum -c MANIFEST.sha256
```

- [ ] **Step 3: Build deterministic distributions twice**

```bash
rm -rf dist build src/*.egg-info
export SOURCE_DATE_EPOCH="$(git show -s --format=%ct HEAD)"
python -m build
sha256sum dist/* > .prelaunch-corrective/candidate/dist-pass1.sha256
rm -rf dist build src/*.egg-info
python -m build
sha256sum dist/* > .prelaunch-corrective/candidate/dist-pass2.sha256
diff -u .prelaunch-corrective/candidate/dist-pass1.sha256 .prelaunch-corrective/candidate/dist-pass2.sha256
python scripts/verify_distribution.py --dist-dir dist
```

Expected: byte-identical deterministic build and verifier PASS.

- [ ] **Step 4: Prove retired current-tree identities are absent**

Run byte-safe text scan over `git ls-files`; expected zero hits except fragmented negative-test construction that never contains the retired literals.

- [ ] **Step 5: Commit final tree normalization**

```text
build(package): finalize deterministic v1.0.0 source and distribution manifests

- Regenerate the tracked source manifest after the canonical namespace and documentation relocation are complete.
- Verify deterministic wheel and sdist construction against canonical v1.0.0 metadata and package contents.
- Record a clean candidate tree with full regression, publication, naming, and documentation gates passing.
```

---

### Task 9: Reconstruct the Entire Public Git History With Modern Messages

**Files:**
- Create (executor-only, not final tree): `.prelaunch-corrective/history/history-before.tsv`
- Create: `.prelaunch-corrective/history/history-after.tsv`
- Create: `.prelaunch-corrective/history/rewrite-map.tsv`
- Create: `.prelaunch-corrective/history/messages/NN.txt`

**Interfaces:**
- History generator consumes old commits oldest→newest and candidate logical patches, then creates commits with explicit `GIT_AUTHOR_*`/`GIT_COMMITTER_*` metadata.

- [ ] **Step 1: Export original history and per-commit diffs**

```bash
git log --reverse --format='%H%x09%an%x09%ae%x09%aI%x09%cn%x09%ce%x09%cI%x09%s' > .prelaunch-corrective/history/history-before.tsv
for sha in $(git rev-list --reverse main); do
  git show --format=fuller --stat --numstat "$sha" > ".prelaunch-corrective/history/${sha}.review.txt"
done
```

- [ ] **Step 2: Curate every retained commit body from its actual diff**

Every message must use subject + blank line + at least two `- ` bullets. Retained early logical boundaries keep their exact original timestamps. Recommended subject sequence for retained foundations:

```text
feat(engine): establish embedding and reranking foundations
feat(runtime): add CPU safety and configuration controls
feat(api): add authenticated REST and operator workflows
test(runtime): qualify engine and API contracts
test(runtime): qualify recovery and lifecycle behavior
perf(int8): add INT8 quantization candidate coverage
perf(int8): add repeatable performance benchmark harness
feat(reranker): add GGUF and llama.cpp integration
feat(reranker): harden native instruction transport
feat(qdrant): integrate the production-demo retrieval pipeline
test(production): qualify K=5 retrieval and reranking
build(package): prepare the first public v1.0.0 distribution
refactor(identity): adopt the canonical project and package identity
docs: organize bilingual project documentation
docs(readme): build complete bilingual project landing pages
test(publication): align notebook and publication guards with the canonical layout
ci(release): modernize GitHub Actions and package validation
build(package): finalize deterministic v1.0.0 source and distribution manifests
```

For each subject, bullets must be copied/derived from the reviewed changed-file/stat evidence; generic filler is rejected by the history-quality gate.

- [ ] **Step 3: Assign split-commit timestamps**

Retained first 12 logical boundaries keep original timestamps. Newly split publication commits use strictly increasing timestamps between `2026-09-04T09:06:47Z` and `2026-09-05T07:06:29Z`, with the final reconstructed commit retaining `2026-09-05T07:06:29Z`.

- [ ] **Step 4: Build the rewritten chain with explicit metadata**

Use `git commit-tree` or an equivalent scripted rebase that sets:

```bash
GIT_AUTHOR_NAME='Đăng Khoa'
GIT_AUTHOR_EMAIL='i.am@dangkhoa.dev'
GIT_AUTHOR_DATE='<curated ISO timestamp>'
GIT_COMMITTER_NAME='Đăng Khoa'
GIT_COMMITTER_EMAIL='i.am@dangkhoa.dev'
GIT_COMMITTER_DATE='<curated ISO timestamp>'
```

Do not use GitHub Contents API for reconstructed commits because it cannot satisfy the timestamp-preservation contract.

- [ ] **Step 5: Run history-quality verification**

Assert:

```text
all commits author/committer identity exact
strict chronological order
subject matches allowed type/scope syntax
blank line after subject
>=2 bullet body lines per commit
no generic bodies such as "update files", "cleanup", "misc changes"
no single reconstructed commit recreates the 76-file mixed-responsibility tip
final reconstructed tree == verified candidate tree
```

- [ ] **Step 6: Do not push yet**

Create a local branch `prelaunch-reconstructed-v1.0.0` and record its SHA/tree for independent review.

---

### Task 10: Final Pre-Push Review and CI-Equivalent Verification

**Files:**
- Generated: `.prelaunch-corrective/final-prepush/`

- [ ] **Step 1: Compare reconstructed final tree to verified candidate tree**

```bash
test "$(git rev-parse prelaunch-reconstructed-v1.0.0^{tree})" = "<verified-candidate-tree-from-task-8>"
```

The executor must substitute the captured Task 8 tree SHA, not a manually guessed value.

- [ ] **Step 2: Check full history messages and metadata**

Export `history-after.tsv`; compare author/committer identity and retained dates to `history-before.tsv` according to the mapping.

- [ ] **Step 3: Run full tests/build from the reconstructed branch**

```bash
git switch prelaunch-reconstructed-v1.0.0
PYTHONPATH=src pytest -q
python scripts/check-canonical-model-naming.py .
python scripts/validate-publication-notebook.py notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb
sha256sum -c MANIFEST.sha256
rm -rf dist build src/*.egg-info
export SOURCE_DATE_EPOCH="$(git show -s --format=%ct HEAD)"
python -m build
python scripts/verify_distribution.py --dist-dir dist
```

- [ ] **Step 4: Independent secret scan**

Scan tracked tree, commit messages, generated evidence JSON/text, and remote URLs. Do not print matched credential plaintext; report only path/type and a non-reversible fingerprint if needed.

Expected: all gates PASS before any public mutation.

---

### Task 11: Controlled Main Rewrite, Ruleset Restoration, and Main CI Gate

**Files:**
- Generated evidence: `.prelaunch-corrective/publication/main/`

- [ ] **Step 1: Re-fetch live preconditions immediately before mutation**

Require live `main`, ruleset 22445904, tag object, and release asset digests to match the Task 1 freeze or explicitly re-freeze and review any legitimate drift. Abort on unexplained drift.

- [ ] **Step 2: Temporarily disable only ruleset 22445904**

Capture before/disabled JSON. Do not alter unrelated governance.

- [ ] **Step 3: Force-update main with lease/precondition protection**

```bash
git push --force-with-lease=refs/heads/main:<frozen-main-sha> origin prelaunch-reconstructed-v1.0.0:main
```

- [ ] **Step 4: Restore ruleset immediately**

Require enforcement `active`, no bypass, strict required checks `Package`, `Quality / Python 3.10`, `Quality / Python 3.12`.

- [ ] **Step 5: Wait for and audit main CI**

Require all three jobs success and correct new head SHA. On failure, do not recreate the tag or release.

---

### Task 12: Recreate v1.0.0, Tag CI, Artifact, and GitHub Release

**Files:**
- Generated evidence: `.prelaunch-corrective/publication/tag-release/`

- [ ] **Step 1: Recreate annotated tag only after main CI PASS**

Create `v1.0.0` targeting new main. Preserve tagger identity `Đăng Khoa <i.am@dangkhoa.dev>` and use the canonical tag message:

```text
Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant v1.0.0
```

- [ ] **Step 2: Require tag CI PASS**

Require strict manifest verification and canonical tag distribution upload.

- [ ] **Step 3: Download the new Actions artifact and independently verify it**

Require artifact name:

```text
qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant-v1.0.0-dist
```

Verify wheel/sdist metadata, namespace, deterministic hashes, and sidecars.

- [ ] **Step 4: Replace release assets from the new tag artifact only**

No old distribution files remain attached.

- [ ] **Step 5: Update GitHub Release metadata**

Set title exactly:

```text
v1.0.0
```

Set body from `docs/releases/v1.0.0.md`. Keep `draft=false`, `prerelease=false`, immutable releases disabled unless separately approved, and do not create tag protection unless separately approved.

- [ ] **Step 6: Download all final release assets and compare byte-for-byte**

Every downloaded release asset must match the canonical tag CI artifact/sidecar source.

---

### Task 13: Forensic Evidence Bundle and Acceptance

**Files:**
- Generate: `/tmp/qwen3-prelaunch-repository-corrective-<UTC>.zip`
- Generate: matching `.sha256`

- [ ] **Step 1: Assemble only necessary evidence**

Include baseline/final GitHub JSON, history before/after/rewrite map, commit-message audit, test/build outputs, manifest checks, main/tag CI JSON/jobs, artifact metadata, release metadata, release-download hashes, ruleset before/disable/restore/final, and terminal log. Exclude venv, caches, model weights, Qdrant snapshots, and credentials.

- [ ] **Step 2: Verify evidence archive**

```bash
sha256sum <archive> > <archive>.sha256
unzip -t <archive>
```

- [ ] **Step 3: Secret-scan the final evidence archive**

Expected: no PAT-like token, bearer secret, credential-bearing remote URL, or `.env` secret value.

- [ ] **Step 4: Final acceptance output**

Only when archive and live GitHub state agree, emit:

```text
PRELAUNCH_REPOSITORY_CORRECTIVE=ACCEPTED
CANONICAL_IDENTITY=PASS
DOCUMENTATION_STRUCTURE=PASS
BILINGUAL_README=PASS
GITHUB_ACTIONS_POLICY=PASS
FULL_HISTORY_REWRITE=PASS
MAIN_CI=PASS
TAG_V1.0.0=PASS
TAG_CI=PASS
RELEASE_TITLE=v1.0.0
RELEASE_ASSETS=PASS
PUBLICATION_READY=YES
NEXT=FRESH_KAGGLE_PRODUCTION_DEMO_AND_PUBLIC_NOTEBOOK_EVIDENCE
```

Fresh Kaggle remains blocked until this exact acceptance is independently audited.
