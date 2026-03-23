#!/usr/bin/env python3
import argparse
import filecmp
import pathlib
import shutil
import subprocess
import sys
import tempfile


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW_SPEC_PATH = REPO_ROOT / "openapi" / "raw" / "justserpapi-openapi.json"
NORMALIZED_SPEC_PATH = REPO_ROOT / "openapi" / "normalized" / "justserpapi-openapi.json"
GENERATED_SOURCE_PATH = REPO_ROOT / "src" / "main" / "generated"


def run(command):
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def compare_directories(left: pathlib.Path, right: pathlib.Path) -> bool:
    comparison = filecmp.dircmp(left, right)
    if comparison.left_only or comparison.right_only or comparison.diff_files or comparison.funny_files:
        return False
    return all(compare_directories(left / directory, right / directory) for directory in comparison.common_dirs)


def sync_generated_sources(source_dir: pathlib.Path, destination_dir: pathlib.Path) -> None:
    if destination_dir.exists():
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch, normalize, and regenerate the JustSerpAPI Java SDK.")
    parser.add_argument("--skip-fetch", action="store_true", help="Reuse the checked-in raw OpenAPI spec.")
    parser.add_argument("--check", action="store_true", help="Verify that the checked-in generated sources are up to date.")
    args = parser.parse_args()

    if not args.skip_fetch:
        run([sys.executable, "scripts/fetch_openapi.py", "--output", str(RAW_SPEC_PATH)])

    run([sys.executable, "scripts/normalize_openapi.py", "--input", str(RAW_SPEC_PATH), "--output", str(NORMALIZED_SPEC_PATH)])

    with tempfile.TemporaryDirectory(prefix="justserpapi-codegen-") as temp_dir_name:
        output_dir = pathlib.Path(temp_dir_name) / "generated-sdk"
        run([
            "mvn",
            "-q",
            "-Pcodegen",
            "-DskipTests",
            f"-Dopenapi.codegen.outputDir={output_dir}",
            "generate-sources"
        ])

        generated_root = output_dir / "src" / "main" / "generated"
        if not generated_root.exists():
            raise FileNotFoundError(f"Expected generated sources under {generated_root}")

        if args.check:
            if not GENERATED_SOURCE_PATH.exists():
                print(f"Missing generated source directory: {GENERATED_SOURCE_PATH}", file=sys.stderr)
                return 1
            if not compare_directories(generated_root, GENERATED_SOURCE_PATH):
                print("Generated sources are out of date. Run scripts/sync_sdk.py to refresh them.", file=sys.stderr)
                return 1
            return 0

        sync_generated_sources(generated_root, GENERATED_SOURCE_PATH)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
