"""
vcf_subsample.py — Stratified VCF subsampler (every Nth variant)

Takes every Nth variant across the full VCF to ensure geographic spread
across the chromosome rather than clustering at the start.

Usage:
    python scripts/vcf_subsample.py --input <vcf> --output <vcf> --n <int>

Example:
    python scripts/vcf_subsample.py \
        --input data/raw/ALL.chr21.GRCh38.phased.vcf \
        --output data/demo/chr21_subsampled.vcf \
        --n 100
"""

import argparse
from pathlib import Path


def subsample_vcf(input_path: Path, output_path: Path, n: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    kept = 0

    print(f"Streaming {input_path} ...")

    with open(input_path, "r") as fin, open(output_path, "w") as fout:
        for line in fin:
            if line.startswith("#"):
                fout.write(line)
                continue

            if total % n == 0:
                fout.write(line)
                kept += 1

            total += 1

            if total % 500_000 == 0:
                print(f"  {total:,} variants scanned, {kept:,} kept ...")

    print(f"\nTotal variants scanned : {total:,}")
    print(f"Variants kept (every {n}): {kept:,}")
    print(f"Written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Stratified VCF subsampler — keeps every Nth variant"
    )
    parser.add_argument("--input", required=True, type=Path, help="Input VCF path")
    parser.add_argument("--output", required=True, type=Path, help="Output VCF path")
    parser.add_argument("--n", required=True, type=int, help="Keep every Nth variant")
    args = parser.parse_args()

    subsample_vcf(args.input, args.output, args.n)


if __name__ == "__main__":
    main()
