# news-image-20261120 entry runner
# Places the bundled artwork where the grading harness expects it.
# Uses only the Python standard library so it runs anywhere Python 3.13 does.

import os
import sys
from pathlib import Path


def locate_bundled_artwork() -> Path:
    """Return the path of the image shipped beside this script."""
    script_folder = Path(__file__).resolve().parent
    return script_folder / "entry.png"


def resolve_destination_folder() -> Path:
    """Pick the output folder from the environment, with a sane fallback."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if configured:
        return Path(configured)
    return Path("/output")


def transfer_artwork(source_path: Path, target_folder: Path) -> Path:
    """Copy the artwork bytes into the destination folder."""
    target_folder.mkdir(parents=True, exist_ok=True)
    destination_path = target_folder / "entry.png"
    payload = source_path.read_bytes()
    destination_path.write_bytes(payload)
    return destination_path


def run() -> int:
    artwork = locate_bundled_artwork()
    if not artwork.is_file():
        print(f"error: bundled image not found at {artwork}", file=sys.stderr)
        return 1
    if artwork.stat().st_size == 0:
        print(f"error: bundled image is empty at {artwork}", file=sys.stderr)
        return 1
    folder = resolve_destination_folder()
    written = transfer_artwork(artwork, folder)
    print(f"wrote {written} ({written.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
