from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/qwen3_embedding_reranker_qdrant_kaggle_demo.ipynb"

def _notebook():
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))

def test_publication_ready_notebook_contract():
    nb = _notebook()
    text = "\n".join("".join(c.get("source", [])) for c in nb["cells"])

    family = "Qwen" + "3"
    standalone = re.compile(r"(?<![-\w])" + family + r"(?![-\w])")
    assert not standalone.search(text)

    for banned in [
        "DIAG_" + "CELL3",
        "mount " + "corrective",
        "v7 " + "diagnostics",
        "v8-" + "mount-corrective",
    ]:
        assert banned not in text

    for unsafe in ["pkill ", "killall ", "fuser -k", "lsof -t"]:
        assert unsafe not in text

    for required in [
        "Qwen3-Embedding-4B / Qwen3-Reranker-4B and Qdrant Stack - v1.0.0",
        "dangkhoa2016/qwen-qwen3-embedding-4b",
        "dangkhoa2016/giladgd-qwen3-reranker-4b-gguf",
        "dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k",
        "dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime",
        "/kaggle/input/datasets",
        "RUNTIME-MANIFEST.sha256",
        "RUNTIME_LOCATOR_MODE=EXACT_NAMESPACED_PATH",
        "RUNTIME_LOCATOR_MODE=RECURSIVE_DATASETS_NAMESPACE",
        "LLAMA_CPP_SETUP=PASS_EXISTING_BINARY",
        "QUALIFIED_LLAMA_RUNTIME_INPUT=PASS",
        "LLAMA_EXECUTING_PROCESS_AND_MAPPED_IMPLEMENTATION=PASS",
        "PRODUCTION_QUALIFICATION=PASS",
        "PRIOR_RUN_CLEANUP_BEGIN",
        "PRIOR_RUN_CLEANUP=PASS",
        "PRIOR_RUN_UNOWNED_PORT=FAIL",
        "PRIOR_RUN_OWNED_PROCESSES_STOPPED",
        "PRIOR_RUN_WORKSPACE_RESET=PASS",
        "qualification-owner.json",
        "hybrid-server.pid",
        "llama-server.pid",
        "_same_process_starttime",
        "_assert_ports_free",
    ]:
        assert required in text, required

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            assert cell.get("execution_count") is None
            assert cell.get("outputs") == []

def test_owned_process_predicates_are_fail_closed():
    nb = _notebook()
    cleanup = next(
        "".join(c.get("source", []))
        for c in nb["cells"]
        if c.get("cell_type") == "code"
        and "PRIOR_RUN_CLEANUP_BEGIN" in "".join(c.get("source", []))
    )
    tree = ast.parse(cleanup)
    keep = [
        node for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
    ]
    module = ast.Module(body=keep, type_ignores=[])
    ast.fix_missing_locations(module)
    ns = {}
    exec(compile(module, "<cleanup-functions>", "exec"), ns)

    def write_proc(proc_root, pid, *, cwd, args, exe=None, environ=None, maps=""):
        p = proc_root / str(pid)
        p.mkdir(parents=True)
        tail = ["S"] + ["0"] * 18 + ["424242"] + ["0"] * 6
        (p / "stat").write_text(f"{pid} (owned-test) " + " ".join(tail))
        (p / "cmdline").write_bytes(b"\0".join(a.encode() for a in args) + b"\0")
        (p / "cwd").symlink_to(cwd)
        if exe is not None:
            (p / "exe").symlink_to(exe)
        env = environ or {}
        (p / "environ").write_bytes(
            b"\0".join(f"{k}={val}".encode() for k, val in env.items()) + b"\0"
        )
        (p / "maps").write_text(maps)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        proc = td / "proc"; proc.mkdir()
        app = td / "repo"; app.mkdir()
        other = td / "other"; other.mkdir()
        qdrant_exe = td / "qdrant"; qdrant_exe.write_bytes(b"qdrant")
        launcher = td / "llama-server-patched"; launcher.write_bytes(b"launcher")
        impl = td / "libllama-server-impl.so"; impl.write_bytes(b"impl")
        storage = td / "run/qdrant/storage"; storage.mkdir(parents=True)

        ns.update({
            "PROC_ROOT": proc,
            "APP_ROOT": app,
            "EXPECTED_QDRANT_EXE": qdrant_exe,
            "EXPECTED_QDRANT_STORAGE": storage,
            "EXPECTED_GGUF_NAME": "Qwen3-Reranker-4B.Q4_K_M.gguf",
            "EXPECTED_LAUNCHER_SHA": hashlib.sha256(launcher.read_bytes()).hexdigest(),
        })

        write_proc(proc, 101, cwd=app, args=[
            "python", "-m", "uvicorn", "qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant.main:app",
            "--port", "8000",
        ])
        assert ns["_is_owned_hybrid"](101)
        assert ns["_same_process_starttime"](101, 424242)

        write_proc(proc, 102, cwd=other, args=[
            "python", "-m", "uvicorn", "qwen3_embedding_4b_and_qwen3_reranker_4b_with_qdrant.main:app",
            "--port", "8000",
        ])
        assert not ns["_is_owned_hybrid"](102)

        write_proc(proc, 201, cwd=app, args=[str(qdrant_exe)], exe=qdrant_exe,
                   environ={
                       "QDRANT__STORAGE__STORAGE_PATH": str(storage),
                       "QDRANT__SERVICE__HTTP_PORT": "6333",
                       "QDRANT__SERVICE__HOST": "127.0.0.1",
                   })
        assert ns["_is_owned_qdrant"](201)

        write_proc(proc, 202, cwd=app, args=[str(qdrant_exe)], exe=qdrant_exe,
                   environ={
                       "QDRANT__STORAGE__STORAGE_PATH": str(td / "foreign"),
                       "QDRANT__SERVICE__HTTP_PORT": "6333",
                       "QDRANT__SERVICE__HOST": "127.0.0.1",
                   })
        assert not ns["_is_owned_qdrant"](202)

        write_proc(proc, 301, cwd=app, exe=launcher, args=[
            str(launcher), "--model", "/models/Qwen3-Reranker-4B.Q4_K_M.gguf",
            "--port", "8081",
        ], maps=f"1-2 r-xp 0 00:00 0 {impl}\n")
        assert ns["_is_owned_llama"](301)

        write_proc(proc, 302, cwd=app, exe=launcher, args=[
            str(launcher), "--model", "/models/Qwen3-Reranker-4B.Q4_K_M.gguf",
            "--port", "9999",
        ], maps=f"1-2 r-xp 0 00:00 0 {impl}\n")
        assert not ns["_is_owned_llama"](302)

        candidates = set()
        ns["_add_if_verified"](candidates, 102, "hybrid-api", ns["_is_owned_hybrid"])
        assert candidates == set()
        ns["_add_if_verified"](candidates, 101, "hybrid-api", ns["_is_owned_hybrid"])
        assert candidates == {101}


def test_canonical_naming_guard_distinguishes_standalone_word_from_technical_identifier(tmp_path):
    guard = ROOT / "scripts/check-canonical-model-naming.py"

    (tmp_path / "technical.py").write_text(
        'ARCH = "Qwen3ForCausalLM"\n', encoding="utf-8"
    )
    ok = subprocess.run(
        [sys.executable, str(guard), str(tmp_path)],
        text=True, capture_output=True,
    )
    assert ok.returncode == 0, ok.stdout + ok.stderr

    family = "Qwen" + "3"
    (tmp_path / "public.md").write_text(
        f"Standalone {family} wording is not canonical.\n", encoding="utf-8"
    )
    bad = subprocess.run(
        [sys.executable, str(guard), str(tmp_path)],
        text=True, capture_output=True,
    )
    assert bad.returncode != 0
    assert "standalone model-family token" in bad.stdout


def test_internal_label_guard_does_not_flag_test_fixture_source(tmp_path):
    guard = ROOT / "scripts/check-canonical-model-naming.py"
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_fixture.py").write_text(
        'value = "STAGE2" + "_R10"\n', encoding="utf-8"
    )
    result = subprocess.run(
        [sys.executable, str(guard), str(tmp_path)],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
