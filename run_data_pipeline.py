"""Safe entry point: public steps only unless restricted use is explicit."""

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PUBLIC_DOWNLOADS = [
    "download_small_area_census.py",
    "download_census_glossary.py",
    "download_small_area_boundaries.py",
    "download_uk_need_sample.py",
]
PUBLIC_PROCESSING = [
    "process_small_area_features.py",
    "build_small_area_spatial_features.py",
    "build_spatial_model_features.py",
    "process_uk_need_sample.py",
    "validate_research_datasets.py",
    "assess_ml_readiness.py",
]


def run(script, *arguments):
    command = [sys.executable, str(ROOT / "scripts" / script), *map(str, arguments)]
    print("RUN", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="refresh official public downloads")
    parser.add_argument("--include-restricted", action="store_true")
    parser.add_argument("--restricted-path", type=Path)
    parser.add_argument("--restricted-validation-report", type=Path)
    args = parser.parse_args()

    if args.include_restricted and not args.restricted_path:
        parser.error("--include-restricted requires --restricted-path")
    if args.restricted_path and not args.include_restricted:
        parser.error("--restricted-path requires --include-restricted")

    if args.download:
        for script in PUBLIC_DOWNLOADS:
            run(script)
    for script in PUBLIC_PROCESSING:
        run(script)

    if args.include_restricted:
        report = args.restricted_validation_report or (ROOT / "outputs" / "reports" / "restricted_validation.json")
        run("restricted/prepare_metered_energy_model_input.py", "--secure-input", args.restricted_path, "--validation-report", report)


if __name__ == "__main__":
    main()
