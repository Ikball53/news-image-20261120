#!/usr/bin/env python3
"""Copy the bundled news image to the make.fun output directory."""

import os
import shutil
import sys


def resolve_output_dir() -> str:
    """Return the grader output directory, defaulting to /output."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return configured if configured else "/output"


def main() -> int:
    # The image always sits next to this script in the repository root.
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source_image = os.path.join(repo_dir, "entry.png")
    output_dir = resolve_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source_image, destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
