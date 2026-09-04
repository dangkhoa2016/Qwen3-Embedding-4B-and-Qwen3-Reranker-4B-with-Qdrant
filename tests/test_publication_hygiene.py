from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    path = ROOT / name
    assert path.is_file(), f"missing publication file: {name}"
    return path.read_text(encoding="utf-8")


def test_instruction_capacity_is_1024():
    assert "MAX_INSTRUCTION_CHARS=1024" in read(".env.example")


def test_public_docs_record_verified_k5_default_without_internal_labels():
    for name in (
        "README.md",
        "docs/production-demo/overview.md",
        "docs/production-demo/overview.vi.md",
        "docs/production-demo/guide.md",
        "docs/production-demo/qualification.md",
    ):
        text = read(name)
        assert "K=5" in text, name
        assert "K5" + "_DEFAULT=ACCEPT" not in text, name
        assert "K2" + "_FALLBACK=NOT_JUSTIFIED" not in text, name


def test_public_production_qualification_record_is_present():
    text = read("docs/production-demo/qualification.md")
    assert "Production qualification: PASS" in text
    assert "Retrieval default: K=5" in text
    assert "Semantic validation: 3/3 PASS" in text
    assert "Verified Run All: 469.782s" in text


def test_obsolete_publication_checkpoint_files_are_absent_from_current_tree():
    legacy = "PRE" + "_PUBLISH_NOTES"
    assert not (ROOT / f"{legacy}.md").exists()
    assert not (ROOT / f"{legacy}.vi.md").exists()


def test_no_egg_info_residue_in_source_tree():
    assert not list((ROOT / "src").glob("*.egg-info"))


def test_release_notes_are_github_release_focused_and_bilingual():
    release_en = read("docs/releases/v1.0.0.md")
    release_vi = read("docs/releases/v1.0.0.vi.md")
    h1 = "# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant - v1.0.0"

    assert release_en.startswith(h1 + "\n")
    assert release_vi.startswith(h1 + "\n")
    assert "## Production qualification" in release_en
    assert "## Verification" in release_en
    assert "## Kiểm chứng production" in release_vi
    assert "## Xác minh" in release_vi

    for text in (release_en, release_vi):
        assert "PyPI" not in text
        assert "TAG=NONE" not in text
        assert "RELEASE=NONE" not in text
        assert "first-release tag and GitHub Release pending" not in text
        assert "no `v1.0.0` tag or GitHub Release has been created yet" not in text
