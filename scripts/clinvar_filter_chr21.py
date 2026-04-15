"""
clinvar_filter_chr21.py — Stream ClinVar and keep only GRCh38 chr21 rows

Streams variant_summary.txt line by line — never loads the full file
into memory. Safe to run on machines with limited RAM.

Usage:
    python scripts/clinvar_filter_chr21.py

Output:
    data/processed/clinvar_chr21.csv
"""

import csv

from config import DATA_DEMO, DATA_RAW

INPUT_PATH = DATA_RAW / "variant_summary.txt"
OUTPUT_PATH = DATA_DEMO / "clinvar_chr21.tsv"

COLS = [
    "Chromosome",
    "PositionVCF",
    "ReferenceAlleleVCF",
    "AlternateAlleleVCF",
    "ClinicalSignificance",
    "GeneSymbol",
    "PhenotypeList",
    "Assembly",
    "VariationID",
]


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    kept = 0
    total = 0

    print(f"Streaming {INPUT_PATH} ...")

    with open(INPUT_PATH, "r") as fin, open(OUTPUT_PATH, "w", newline="") as fout:
        reader = csv.DictReader(fin, delimiter="\t")
        writer = csv.DictWriter(fout, fieldnames=COLS, delimiter="\t")
        writer.writeheader()

        for row in reader:
            total += 1

            if row["Assembly"] == "GRCh38" and row["Chromosome"] == "21":
                writer.writerow({c: row[c] for c in COLS})
                kept += 1

            if total % 500_000 == 0:
                print(f"  {total:,} rows scanned, {kept:,} kept ...")

    print(f"\nDone. {kept:,} chr21 GRCh38 rows saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
