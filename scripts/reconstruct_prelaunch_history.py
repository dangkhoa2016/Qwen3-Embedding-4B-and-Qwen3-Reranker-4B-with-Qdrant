#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import re
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[1]
OLD_MAIN = "cf831e90f9e762033b914ba66906fbc710f36bb8"
CANDIDATE = "cd7fcaf5954a7c734bdbae8fbc61bde76ebc4751"
TARGET_BRANCH = "prelaunch-reconstructed-v1.0.0"
IDENTITY_NAME = "Đăng Khoa"
IDENTITY_EMAIL = "i.am@dangkhoa.dev"

EARLY_MESSAGES = [
    ("feat(engine): establish embedding and reranking foundations", [
        "Add the core embedding and reranking engines, shared tensor helpers, formatting, and model-location primitives.",
        "Establish the initial Qwen3 4B inference contracts that later runtime, API, and qualification work builds on.",
    ]),
    ("feat(runtime): add CPU safety and configuration controls", [
        "Introduce memory-aware configuration, startup gates, process locking, and conservative CPU runtime controls.",
        "Keep failure handling explicit so unsupported or unsafe runtime conditions stop before model inference begins.",
    ]),
    ("feat(api): add authenticated REST and operator workflows", [
        "Expose health, readiness, embedding, reranking, model, and statistics endpoints through the FastAPI service.",
        "Add authentication and operator scripts for controlled startup, monitoring, smoke checks, and shutdown.",
    ]),
    ("test(runtime): qualify engine and API contracts", [
        "Add regression coverage for configuration, memory, API, pooling, formatting, model location, and engine behavior.",
        "Lock the expected CPU-oriented service contracts before later optimization and production-demo changes.",
    ]),
    ("test(runtime): qualify recovery and lifecycle behavior", [
        "Exercise repeated startup, process ownership, recovery, readiness, and failure-path behavior under operator workflows.",
        "Verify lifecycle safety without weakening the fail-closed runtime and authentication boundaries.",
    ]),
    ("perf(int8): add INT8 quantization candidate coverage", [
        "Add INT8 quantization helpers, candidate configuration, setup tooling, and focused regression coverage.",
        "Keep quantized experiments isolated from the qualified default runtime so optimization work cannot silently change release semantics.",
    ]),
    ("perf(int8): add repeatable performance benchmark harness", [
        "Add repeatable benchmark clients, campaign runners, monitoring, and result summarization for candidate evaluation.",
        "Separate performance evidence collection from correctness gates so benchmark experiments remain auditable.",
    ]),
    ("feat(reranker): add GGUF and llama.cpp integration", [
        "Integrate GGUF discovery, llama-server lifecycle management, and the native reranker backend.",
        "Add backend-specific validation and tests while retaining the Transformers reranker path for comparison and fallback analysis.",
    ]),
    ("feat(reranker): harden native instruction transport", [
        "Harden instruction serialization and transport across the native llama.cpp reranker boundary.",
        "Add regression coverage for instruction limits, request construction, and native server behavior to prevent semantic drift.",
    ]),
    ("feat(qdrant): integrate the production-demo retrieval pipeline", [
        "Add Qdrant snapshot discovery, restore/setup tooling, production-demo orchestration, and canonical evaluation queries.",
        "Connect embedding retrieval and reranking into one reproducible bilingual search pipeline without reseeding the frozen collection.",
    ]),
    ("test(production): qualify K=5 retrieval and reranking", [
        "Lock K=5 retrieval as the production-demo default and exercise the end-to-end Qdrant retrieval/reranking contract.",
        "Record semantic, timing, memory, and repeated Run All acceptance evidence for the qualified CPU demonstration path.",
    ]),
    ("build(package): prepare the first public v1.0.0 distribution", [
        "Prepare version 1.0.0 package metadata, license, governance files, request limits, and publication-facing source inventory.",
        "Raise the instruction capacity to the qualified 1024-character contract while preserving the accepted production semantics.",
    ]),
]

TAIL_MESSAGES = {
    "identity": ("refactor(identity): adopt the canonical project and package identity", [
        "Rename the Python distribution and import namespace to the full Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant identity.",
        "Update runtime, operator, example, and regression references without changing the qualified embedding, reranking, or Qdrant behavior.",
    ]),
    "docs": ("docs: organize bilingual project documentation", [
        "Move community-health material under .github and production/release material into a navigable docs hierarchy.",
        "Remove historical development documents from the current public tree and keep English/Vietnamese documentation pairs aligned.",
    ]),
    "readme": ("docs(readme): build complete bilingual project landing pages", [
        "Expand both root README files with architecture, setup, API, production qualification, reproducibility, limitations, and release navigation.",
        "Keep English and Vietnamese startup commands, external inputs, model identities, and qualification results technically synchronized.",
    ]),
    "publication": ("test(publication): align notebook and publication guards with the canonical layout", [
        "Align the publication-ready Kaggle notebook, canonical naming guard, documentation topology checks, and relative-link validation with the final layout.",
        "Fail closed on retired identities, internal development labels, broken local links, and publication-contract drift.",
    ]),
    "ci": ("ci(release): modernize GitHub Actions and package validation", [
        "Use current v7 major tags for official GitHub Actions with read-only workflow permissions and blocking Python 3.10/3.12 quality jobs.",
        "Centralize wheel and sdist verification, enforce manifest checks, and upload canonical distributions only from version tags.",
    ]),
    "manifest": ("build(package): finalize deterministic v1.0.0 source and distribution manifests", [
        "Freeze MANIFEST.sha256 over the exact publication-ready tracked tree after identity, documentation, notebook, and CI corrections.",
        "Keep the verified v1.0.0 candidate byte-identical to the accepted final candidate tree before publication history is updated.",
    ]),
}

PUBLICATION_TESTS = {
    "tests/test_canonical_identity_contract.py",
    "tests/test_documentation_topology.py",
    "tests/test_markdown_links.py",
    "tests/test_public_repository_hygiene.py",
    "tests/test_publication_hygiene.py",
    "tests/test_publication_ready_kaggle_notebook.py",
}
CI_PATHS = {
    ".github/workflows/ci.yml",
    "MANIFEST.in",
    "scripts/verify_distribution.py",
    "tests/test_release_identity.py",
}
MANIFEST_PATHS = {"MANIFEST.sha256", "VERIFICATION_SUMMARY.txt"}
README_PATHS = {"README.md", "README.vi.md"}
PUBLICATION_PATHS = {
    "notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb",
    "scripts/check-canonical-model-naming.py",
    "scripts/validate-publication-notebook.py",
    *PUBLICATION_TESTS,
}


def run(*args: str, input_text: str | None = None, env: dict[str, str] | None = None, check: bool = True) -> str:
    completed = subprocess.run(
        args,
        cwd=REPO,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        check=False,
    )
    if check and completed.returncode != 0:
        raise SystemExit(f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stdout}")
    return completed.stdout.strip()


def git(*args: str, **kwargs) -> str:
    return run("git", *args, **kwargs)


def message(subject: str, bullets: list[str]) -> str:
    if len(bullets) < 2:
        raise SystemExit(f"commit body requires at least two bullets: {subject}")
    return subject + "\n\n" + "\n".join(f"- {item}" for item in bullets) + "\n"


def commit_tree(tree: str, parent: str | None, msg: str, author_date: str, committer_date: str) -> str:
    env = os.environ.copy()
    env.update({
        "GIT_AUTHOR_NAME": IDENTITY_NAME,
        "GIT_AUTHOR_EMAIL": IDENTITY_EMAIL,
        "GIT_AUTHOR_DATE": author_date,
        "GIT_COMMITTER_NAME": IDENTITY_NAME,
        "GIT_COMMITTER_EMAIL": IDENTITY_EMAIL,
        "GIT_COMMITTER_DATE": committer_date,
    })
    args = ["git", "commit-tree", tree]
    if parent:
        args += ["-p", parent]
    return run(*args, input_text=msg, env=env)


def classify(path: str) -> str:
    if path in MANIFEST_PATHS:
        return "manifest"
    if path in CI_PATHS:
        return "ci"
    if path in README_PATHS:
        return "readme"
    if path in PUBLICATION_PATHS:
        return "publication"

    # Documentation, governance, and retirement of historical publication material.
    if path.startswith("docs/") or (path.startswith(".github/") and path != ".github/workflows/ci.yml"):
        return "docs"
    if path.endswith(".md") or path in {"BASELINE_PROVENANCE.txt"}:
        return "docs"

    # Everything else in the tail is identity/runtime-path migration or its directly coupled regression update.
    return "identity"


def changed_paths() -> dict[str, list[str]]:
    raw = git("diff", "--name-only", "--no-renames", "-z", f"{BASE}..{CANDIDATE}")
    paths = [p for p in raw.split("\0") if p]
    groups = {name: [] for name in TAIL_MESSAGES}
    for path in paths:
        group = classify(path)
        if group not in groups:
            raise SystemExit(f"unclassified path: {path}")
        groups[group].append(path)
    flattened = [p for values in groups.values() for p in values]
    if sorted(flattened) != sorted(paths) or len(flattened) != len(set(flattened)):
        raise SystemExit("tail path classification is incomplete or overlapping")
    for name, values in groups.items():
        if not values:
            raise SystemExit(f"empty reconstruction group: {name}")
    return groups


def apply_group(parent: str, paths: list[str], subject: str, bullets: list[str], when: str, index: Path) -> str:
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = str(index)
    run("git", "read-tree", parent, env=env)
    patch = git("diff", "--binary", "--no-renames", BASE, CANDIDATE, "--", *paths)
    if not patch:
        raise SystemExit(f"empty patch for {subject}")
    run("git", "apply", "--cached", "--whitespace=nowarn", "-", input_text=patch, env=env)
    tree = run("git", "write-tree", env=env)
    return commit_tree(tree, parent, message(subject, bullets), when, when)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def audit_history(head: str, expected_count: int) -> None:
    commits = git("rev-list", "--reverse", head).splitlines()
    if len(commits) != expected_count:
        raise SystemExit(f"unexpected reconstructed commit count: {len(commits)} != {expected_count}")
    previous: datetime | None = None
    allowed = re.compile(r"^(feat|refactor|test|docs|ci|build|chore|perf)(\([a-z0-9-]+\))?: .+")
    for sha in commits:
        raw = git("show", "-s", "--format=%an%x00%ae%x00%aI%x00%cn%x00%ce%x00%cI%x00%B", sha)
        an, ae, ai, cn, ce, ci, body = raw.split("\x00", 6)
        if (an, ae, cn, ce) != (IDENTITY_NAME, IDENTITY_EMAIL, IDENTITY_NAME, IDENTITY_EMAIL):
            raise SystemExit(f"identity mismatch at {sha}: {(an, ae, cn, ce)!r}")
        lines = body.rstrip().splitlines()
        if not lines or not allowed.fullmatch(lines[0]):
            raise SystemExit(f"invalid subject at {sha}: {lines[:1]}")
        if len(lines) < 4 or lines[1] != "" or sum(line.startswith("- ") for line in lines[2:]) < 2:
            raise SystemExit(f"missing modern bullet body at {sha}")
        current = parse_iso(ci)
        if previous is not None and current <= previous:
            raise SystemExit(f"non-increasing committer chronology at {sha}: {ci}")
        previous = current
    print(f"HISTORY_MESSAGE_FORMAT={len(commits)}/{len(commits)} PASS")
    print("HISTORY_AUTHOR_IDENTITY=PASS")
    print("HISTORY_CHRONOLOGY=PASS")


# Resolve base at import time only after repository checkout exists.
BASE = ""


def main() -> None:
    global BASE
    git("fetch", "origin", "main", "prelaunch-repository-corrective-candidate", "prelaunch-reconstructed-v1.0.0", "--tags", "--force")
    if git("rev-parse", "origin/main") != OLD_MAIN:
        raise SystemExit("live main drifted from the frozen precondition")
    if git("rev-parse", "origin/prelaunch-repository-corrective-candidate") != CANDIDATE:
        raise SystemExit("candidate branch drifted from the authoritative final candidate")

    old = git("rev-list", "--reverse", OLD_MAIN).splitlines()
    if len(old) != 15:
        raise SystemExit(f"expected 15 original commits, found {len(old)}")
    BASE = old[11]
    if BASE != "eca119ba6975da25f3ce907ef342526561760d91":
        raise SystemExit(f"unexpected original commit 12: {BASE}")

    parent: str | None = None
    for position, (old_sha, (subject, bullets)) in enumerate(zip(old[:12], EARLY_MESSAGES), 1):
        tree = git("show", "-s", "--format=%T", old_sha)
        adate = git("show", "-s", "--format=%aI", old_sha)
        cdate = git("show", "-s", "--format=%cI", old_sha)
        parent = commit_tree(tree, parent, message(subject, bullets), adate, cdate)
        if git("show", "-s", "--format=%T", parent) != tree:
            raise SystemExit(f"tree drift while rewriting original commit {position}")
        print(f"REWRITE_{position:02d}={old_sha}->{parent}")

    assert parent is not None
    groups = changed_paths()
    old13_date = parse_iso(git("show", "-s", "--format=%cI", old[12]))
    old14_date = parse_iso(git("show", "-s", "--format=%cI", old[13]))
    old15_date = parse_iso(git("show", "-s", "--format=%cI", old[14]))
    schedule = {
        "identity": old13_date,
        "docs": old13_date + (old14_date - old13_date) / 2,
        "readme": old14_date,
        "publication": old14_date + timedelta(hours=4),
        "ci": old15_date - timedelta(hours=4),
        "manifest": old15_date,
    }
    order = ["identity", "docs", "readme", "publication", "ci", "manifest"]

    with tempfile.TemporaryDirectory(prefix="reconstruct-index-") as tmp:
        index = Path(tmp) / "index"
        for offset, name in enumerate(order, 13):
            subject, bullets = TAIL_MESSAGES[name]
            parent = apply_group(parent, groups[name], subject, bullets, iso(schedule[name]), index)
            print(f"REWRITE_{offset:02d}={name}->{parent} FILES={len(groups[name])}")

    final_tree = git("show", "-s", "--format=%T", parent)
    candidate_tree = git("show", "-s", "--format=%T", CANDIDATE)
    if final_tree != candidate_tree:
        residual = git("diff", "--name-status", parent, CANDIDATE)
        raise SystemExit(f"FINAL_TREE_MISMATCH reconstructed={final_tree} candidate={candidate_tree}\n{residual}")
    print(f"FINAL_TREE={final_tree} PASS")

    audit_history(parent, 18)

    lease = git("rev-parse", "origin/prelaunch-reconstructed-v1.0.0")
    result = run(
        "git", "push", "--force-with-lease=refs/heads/prelaunch-reconstructed-v1.0.0:" + lease,
        "origin", parent + ":refs/heads/prelaunch-reconstructed-v1.0.0", check=False,
    )
    print(result)
    if "rejected" in result.lower() or "error:" in result.lower():
        raise SystemExit("RECONSTRUCTED_BRANCH_PUSH=FAIL")
    print(f"RECONSTRUCTED_HEAD={parent}")
    print("RECONSTRUCTED_BRANCH_PUSH=PASS")


if __name__ == "__main__":
    main()
