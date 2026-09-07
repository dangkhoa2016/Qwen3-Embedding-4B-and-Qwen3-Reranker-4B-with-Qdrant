from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    ".github/CONTRIBUTING.md",
    ".github/CONTRIBUTING.vi.md",
    ".github/SECURITY.md",
    ".github/SECURITY.vi.md",
    "docs/README.md",
    "docs/README.vi.md",
    "docs/production-demo/overview.md",
    "docs/production-demo/overview.vi.md",
    "docs/production-demo/guide.md",
    "docs/production-demo/guide.vi.md",
    "docs/production-demo/qualification.md",
    "docs/production-demo/qualification.vi.md",
    "docs/production-demo/provenance.md",
    "docs/production-demo/provenance.vi.md",
    "docs/production-demo/roadmap.md",
    "docs/production-demo/roadmap.vi.md",
    "docs/releases/v1.0.0.md",
    "docs/releases/v1.0.0.vi.md",
]

RETIRED_ROOT_DOCS = [
    "CONTRIBUT" + "ING.md",
    "CONTRIBUT" + "ING.vi.md",
    "SECUR" + "ITY.md",
    "SECUR" + "ITY.vi.md",
    "README_PRODUCTION_" + "DEMO.md",
    "README_PRODUCTION_" + "DEMO.vi.md",
    "guide-production-" + "demo.md",
    "guide-production-" + "demo.vi.md",
    "PRODUCTION_QUALI" + "FICATION.md",
    "PRODUCTION_QUALI" + "FICATION.vi.md",
    "PRODUCTION_DEMO_PROVE" + "NANCE.md",
    "PRODUCTION_DEMO_PROVE" + "NANCE.vi.md",
    "RELEASE_NOTES_" + "v1.0.0.md",
    "RELEASE_NOTES_" + "v1.0.0.vi.md",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_public_documentation_is_organized_under_docs_and_github():
    for path in TARGETS:
        assert (ROOT / path).is_file(), path
    for path in RETIRED_ROOT_DOCS:
        assert not (ROOT / path).exists(), path


def test_readmes_are_full_landing_pages_with_clickable_navigation():
    required_en = [
        "## Overview", "## Architecture", "## Capabilities", "## Production qualification",
        "## Requirements and external inputs", "## Installation", "## Quick start", "## API overview",
        "## Production demo", "## Reproducibility and provenance", "## Documentation", "## Development and verification",
        "## Security", "## Contributing", "## Known limitations", "## Release", "## License",
        "[Documentation](docs/README.md)",
        "[Production demo](docs/production-demo/overview.md)",
        "[Execution guide](docs/production-demo/guide.md)",
        "[Production qualification](docs/production-demo/qualification.md)",
        "[Provenance](docs/production-demo/provenance.md)",
        "[v1.0.0 release notes](docs/releases/v1.0.0.md)",
        "[Security](.github/SECURITY.md)",
        "[Contributing](.github/CONTRIBUTING.md)",
    ]
    required_vi = [
        "## Tổng quan", "## Kiến trúc", "## Khả năng", "## Kiểm chứng production",
        "## Yêu cầu và external inputs", "## Cài đặt", "## Khởi động nhanh", "## Tổng quan API",
        "## Production demo", "## Khả năng tái hiện và nguồn gốc", "## Tài liệu", "## Phát triển và kiểm chứng",
        "## Bảo mật", "## Đóng góp", "## Hạn chế đã biết", "## Phát hành", "## Giấy phép",
        "[Tài liệu](docs/README.vi.md)",
        "[Production demo](docs/production-demo/overview.vi.md)",
        "[Hướng dẫn thực thi](docs/production-demo/guide.vi.md)",
        "[Kiểm chứng production](docs/production-demo/qualification.vi.md)",
        "[Nguồn gốc](docs/production-demo/provenance.vi.md)",
        "[Release notes v1.0.0](docs/releases/v1.0.0.vi.md)",
        "[Bảo mật](.github/SECURITY.vi.md)",
        "[Đóng góp](.github/CONTRIBUTING.vi.md)",
    ]
    en, vi = read("README.md"), read("README.vi.md")
    for value in required_en:
        assert value in en, value
    for value in required_vi:
        assert value in vi, value
    for command in ["set -a", "source .env", "set +a", "bash scripts/start-server.sh"]:
        assert command in en
        assert command in vi


def test_release_note_identity_and_channel_are_canonical():
    en = read("docs/releases/v1.0.0.md")
    vi = read("docs/releases/v1.0.0.vi.md")
    h1 = "# Qwen3-Embedding-4B and Qwen3-Reranker-4B with Qdrant - v1.0.0"
    assert en.startswith(h1 + "\n")
    assert vi.startswith(h1 + "\n")
    assert "PyPI" not in en
    assert "PyPI" not in vi
