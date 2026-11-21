"""Copy the bundled one-day world-news image to the output directory.

The competition runs this program twice in a sandbox with no network;
both runs must write identical bytes, so the program simply copies the
entry.png that ships in this repository.
"""

import os
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    payload = (here / "entry.png").read_bytes()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.png").write_bytes(payload)


if __name__ == "__main__":
    main()
