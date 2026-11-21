#!/usr/bin/env python3
"""make.fun entry for news-image-20261121.

Copies the pre-built image (entry.png, drawn deterministically by
build_image.py from verified news of Saturday 21 November 2026) to the
output directory. Standard library only; no network; byte-identical
on every run.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
