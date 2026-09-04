#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

path = Path(sys.argv[1])
nb = json.loads(path.read_text(encoding="utf-8"))
text = "\n".join("".join(c.get("source", [])) for c in nb["cells"])

banned = [
    "dia" + "gnostic",
    "cor" + "rective",
    "DIAG" + "_",
    "v7 " + "diagnostics",
    "v" + "8",
    "Stage" + "-II",
    "STAGE" + "2",
    "v0." + "2.3c",
    "0.2." + "3rc1",
]
for token in banned:
    assert token.lower() not in text.lower(), f"publication notebook contains internal token: {token}"

family = "Qwen" + "3"
standalone = re.compile(r"(?<![-\w])" + family + r"(?![-\w])")

for unsafe in ["pkill ", "killall ", "fuser -k", "lsof -t"]:
    assert unsafe not in text, f"unsafe process cleanup primitive in publication notebook: {unsafe}"

for i, cell in enumerate(nb["cells"]):
    source = "".join(cell.get("source", []))
    assert not standalone.search(source), f"standalone model-family token in cell {i}"

required = [
    "PRIOR_RUN_CLEANUP_BEGIN",
    "PRIOR_RUN_CLEANUP=PASS",
    "PRIOR_RUN_UNOWNED_PORT=FAIL",
    "PRIOR_RUN_OWNED_PROCESSES_STOPPED",
    "PRIOR_RUN_WORKSPACE_RESET=PASS",
    "STAGE_3_4_BEGIN",
    "QUALIFICATION_TIMER_AND_CPU_PROFILE=PASS",
    "RUNTIME_PREFLIGHT_BEGIN",
    "RUNTIME_PREFLIGHT=PASS",
    "STAGE_3_4=PASS",
    "qualification-owner.json",
    "hybrid-server.pid",
    "llama-server.pid",
    "_same_process_starttime",
    "_assert_ports_free",
    "Qwen3-Embedding-4B",
    "Qwen3-Reranker-4B",
    "dangkhoa2016/qwen-qwen3-embedding-4b",
    "dangkhoa2016/giladgd-qwen3-reranker-4b-gguf",
    "dangkhoa2016/qdrant-bilingual-search-canonical-v2-1-20k",
    "dangkhoa2016/qwen3-reranker-4b-hardened-llama-cpp-runtime",
    "/kaggle/input/datasets",
    "RUNTIME-MANIFEST.sha256",
    "RUNTIME_LOCATOR_MODE=EXACT_NAMESPACED_PATH",
    "RUNTIME_LOCATOR_MODE=RECURSIVE_DATASETS_NAMESPACE",
    "RUNTIME_MANIFEST=",
    "RUNTIME_COPY=",
    "LLAMA_CPP_SETUP=PASS_EXISTING_BINARY",
    "QUALIFIED_LLAMA_RUNTIME_INPUT=PASS",
    "LLAMA_EXECUTING_PROCESS_AND_MAPPED_IMPLEMENTATION=PASS",
    "ALL_EXPECTED_TOP1_PASS",
    "PRODUCTION_QUALIFICATION=PASS",
]
for marker in required:
    assert marker in text, f"missing publication marker: {marker}"

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    assert cell.get("execution_count") is None, f"code cell {i} has execution_count"
    assert cell.get("outputs") == [], f"code cell {i} has saved outputs"
    assert i > 0 and nb["cells"][i-1]["cell_type"] == "markdown"
    md = "".join(nb["cells"][i-1].get("source", []))
    assert ("**English:**" in md or "**English**" in md), f"missing English guidance before cell {i}"
    assert ("**Tiếng Việt:**" in md or "**Tiếng Việt**" in md), f"missing Vietnamese guidance before cell {i}"


code_sources = [
    "".join(cell.get("source", []))
    for cell in nb["cells"]
    if cell.get("cell_type") == "code"
]
stage_3_4_cells = [source for source in code_sources if "STAGE_3_4_BEGIN" in source]
assert len(stage_3_4_cells) == 1, (
    f"expected exactly one merged stage 3-4 code cell, found {len(stage_3_4_cells)}"
)
stage_3_4 = stage_3_4_cells[0]
for marker in [
    "RUN_ALL_STARTED = time.perf_counter()",
    "QUALIFICATION_TIMER_AND_CPU_PROFILE=PASS",
    "RUNTIME_PREFLIGHT_BEGIN",
    "PIP_EDITABLE_INSTALL",
    "QDRANT_SETUP",
    "RUNTIME_MANIFEST=",
    "LLAMA_SETUP_MODE=PASS_EXISTING_BINARY",
    "RUNTIME_PREFLIGHT=PASS",
    "STAGE_3_4=PASS",
]:
    assert marker in stage_3_4, f"merged stage 3-4 cell missing marker: {marker}"
assert sum("RUN_ALL_STARTED = time.perf_counter()" in source for source in code_sources) == 1
assert sum("RUNTIME_PREFLIGHT_BEGIN" in source for source in code_sources) == 1
print("PUBLICATION_NOTEBOOK_STAGE_3_4_SINGLE_EXECUTION_UNIT=PASS")

print("PUBLICATION_NOTEBOOK_INTERNAL_TERMS=ABSENT PASS")
print("PUBLICATION_NOTEBOOK_CANONICAL_MODEL_NAMING=PASS")
print("PUBLICATION_NOTEBOOK_FOUR_INPUTS=PASS")
print("PUBLICATION_NOTEBOOK_RUNTIME_LOCATOR=PASS")
print("PUBLICATION_NOTEBOOK_RUNTIME_IDENTITIES=PASS")
print("PUBLICATION_NOTEBOOK_QUALIFICATION_GATES=PASS")
print("PUBLICATION_NOTEBOOK_OUTPUTS_CLEAN=PASS")
