"""
vcf_clinvar_filter.py — Filter VCF to ClinVar-matched variants only

Merges a VCF against ClinVar and writes a new VCF containing only
variants with a ClinVar match. Ensures the demo file has full
ClinicalSignificance coverage for a visually complete dashboard.

Usage:
    python scripts/vcf_clinvar_filter.py --input <vcf> --output <vcf>

Example:
    python scripts/vcf_clinvar_filter.py \
        --input data/demo/chr21_subsampled.vcf \
        --output data/demo/demo.vcf
"""

import argparse
from pathlib import Path

import pandas as pd

from config import CLINVAR_PATH
from src.vcf_annotator.parsing.vcf_parser import parse_vcf
from src.vcf_annotator.annotation.clinvar_merge import load_clinvar


def filter_to_clinvar_matches(
    input_path: Path,
    output_path: Path,
    clinvar_path: Path = CLINVAR_PATH,
) -> None:
    print(f"Parsing VCF: {input_path} ...")
    vcf_df, meta = parse_vcf(input_path)

    print(f"Loading ClinVar: {clinvar_path} ...")
    clinvar_df = load_clinvar(clinvar_path)

    print("Merging ...")
    merged = pd.merge(
        vcf_df,
        clinvar_df,
        left_on=["CHROM", "POS", "REF", "ALT"],
        right_on=["Chromosome", "PositionVCF", "ReferenceAlleleVCF", "AlternateAlleleVCF"],
        how="inner",  # inner join — matched variants only
    )

    matched_positions = set(zip(merged["CHROM"], merged["POS"], merged["REF"], merged["ALT"]))

    print(f"Total variants in source : {len(vcf_df):,}")
    print(f"Variants matched ClinVar : {len(matched_positions):,}")

    # Print significance breakdown
    sig_counts = merged["ClinicalSignificance"].value_counts()
    print("\nClinicalSignificance breakdown:")
    print(sig_counts.to_string())

    # Write matched variants back out as a valid VCF
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r") as fin, open(output_path, "w") as fout:
        for line in fin:
            if line.startswith("#"):
                fout.write(line)
                continue

            parts = line.split("\t")
            chrom, pos, ref, alt = parts[0], int(parts[1]), parts[3], parts[4]

            if (str(chrom), pos, ref, alt) in matched_positions:
                fout.write(line)

    print(f"\nWritten to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Filter VCF to ClinVar-matched variants only"
    )
    parser.add_argument("--input",  required=True, type=Path, help="Input VCF path")
    parser.add_argument("--output", required=True, type=Path, help="Output VCF path")
    args = parser.parse_args()

    filter_to_clinvar_matches(args.input, args.output)


if __name__ == "__main__":
    main()
