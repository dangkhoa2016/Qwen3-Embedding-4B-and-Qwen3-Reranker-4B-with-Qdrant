#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
import subprocess

import reconstruct_prelaunch_history as base


def run_bytes(*args: str, input_bytes: bytes | None = None, env: dict[str, str] | None = None) -> bytes:
    completed = subprocess.run(
        args,
        cwd=base.REPO,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        check=False,
    )
    if completed.returncode != 0:
        output = completed.stdout.decode("utf-8", errors="replace")
        raise SystemExit(f"command failed ({completed.returncode}): {' '.join(args)}\n{output}")
    return completed.stdout


def apply_group_bytes(
    parent: str,
    paths: list[str],
    subject: str,
    bullets: list[str],
    when: str,
    index: Path,
) -> str:
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = str(index)
    base.run("git", "read-tree", parent, env=env)
    patch = run_bytes(
        "git", "diff", "--binary", "--no-renames", base.BASE, base.CANDIDATE, "--", *paths
    )
    if not patch:
        raise SystemExit(f"empty patch for {subject}")
    run_bytes(
        "git", "apply", "--cached", "--whitespace=nowarn", "-", input_bytes=patch, env=env
    )
    tree = base.run("git", "write-tree", env=env)
    return base.commit_tree(tree, parent, base.message(subject, bullets), when, when)


if __name__ == "__main__":
    base.apply_group = apply_group_bytes
    base.main()
