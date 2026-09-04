from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_NAME = "Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant"
CANONICAL_SLUG = "Qwen3-Embedding-4B-and-Qwen3-Reranker-4B-with-Qdrant"
DIST_NAME = "qwen3-embedding-4b-and-qwen3-reranker-4b-with-qdrant"
IMPORT_NAME = "qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant"


def test_pyproject_uses_canonical_distribution_name():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["name"] == DIST_NAME
    assert project["version"] == "1.0.0"


def test_python_namespace_and_runtime_identity_are_canonical():
    package = ROOT / "src" / IMPORT_NAME
    assert package.is_dir()
    assert not (ROOT / "src" / ("qwen3" + "_qdrant")).exists()

    namespace = {}
    exec((package / "__init__.py").read_text(encoding="utf-8"), namespace)
    assert namespace["__version__"] == "1.0.0"
    assert namespace["__project_name__"] == DISPLAY_NAME
    assert namespace["__project_slug__"] == CANONICAL_SLUG
    assert namespace["__distribution_name__"] == DIST_NAME


def test_retired_identity_literals_are_absent_from_current_tree():
    retired = (
        "qwen3" + "-embedding-4b-reranker-4b-qdrant",
        "qwen3" + "_embedding_4b_reranker_4b_qdrant",
        "qwen3" + "_qdrant",
    )
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or ".pytest_cache" in path.parts:
            continue
        data = path.read_bytes()
        if b"\0" in data[:8192]:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for value in retired:
            assert value not in text, f"{path.relative_to(ROOT)}: {value}"
