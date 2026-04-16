import pandas as pd

from config import CLINVAR_PATH

ANNOTATED_COLS = [
    "CHROM",
    "POS",
    "REF",
    "ALT",
    "ClinicalSignificance",
    "GeneSymbol",
    "PhenotypeList",
    "ClinVar_URL",
]


def _validate_annotate_cols(df):
    missing = [col for col in ANNOTATED_COLS if col not in df.columns]

    if missing:
        raise ValueError(f"Error: Input VCF missing required columns: {missing}")


def load_clinvar(path=CLINVAR_PATH):
    """
    Load and preprocess the ClinVar variant summary TSV.

    Args:
        path: Path to variant_summary.txt (str or Path)

    Returns:
        DataFrame with relevant ClinVar columns, filtered to GRCh38 assembly
    """
    try:
        clinvar = pd.read_csv(
            path,
            sep="\t",
            usecols=[
                "Chromosome",
                "PositionVCF",
                "ReferenceAlleleVCF",
                "AlternateAlleleVCF",
                "ClinicalSignificance",
                "GeneSymbol",
                "PhenotypeList",
                "Assembly",
                "VariationID",
            ],
            low_memory=False,
        )
    except FileNotFoundError as e:
        raise FileNotFoundError(f"ClinVar file not found: {path}") from e
    except pd.errors.ParserError as e:
        raise ValueError(f"Unable to parse ClinVar file as TSV: {path}") from e

    # Keep only GRCh38 to match standard VCF coordinates
    clinvar = clinvar[clinvar["Assembly"] == "GRCh38"].copy()

    clinvar["Chromosome"] = clinvar["Chromosome"].astype(str)
    clinvar["PositionVCF"] = clinvar["PositionVCF"].astype(int, errors="ignore")

    return clinvar


def annotate(vcf_df, clinvar_df):
    """
    Left-join VCF variants against ClinVar on CHROM, POS, REF, ALT.

    Left join preserves all VCF variants — unmatched rows will have
    NaN for ClinVar columns rather than being silently dropped.

    Args:
        vcf_df:     DataFrame from parse_vcf()
        clinvar_df: DataFrame from load_clinvar()

    Returns:
        Annotated DataFrame with ClinVar columns appended
    """
    if vcf_df is None or clinvar_df is None:
        raise ValueError("vcf_df and clinvar_df must not be None")
    try:
        merged = pd.merge(
            vcf_df,
            clinvar_df,
            left_on=["CHROM", "POS", "REF", "ALT"],
            right_on=[
                "Chromosome",
                "PositionVCF",
                "ReferenceAlleleVCF",
                "AlternateAlleleVCF",
            ],
            how="left",
        )
    except ValueError as e:
        raise ValueError("Unable to merge vcf and clinvar") from e

    # Build direct ClinVar links for matched variants
    merged["ClinVar_URL"] = merged["VariationID"].apply(
        lambda vid: (
            f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{int(vid)}/"
            if pd.notna(vid)
            else None
        )
    )

    # Drop redundant ClinVar key columns (already represented by VCF columns)
    merged.drop(
        columns=[
            "Chromosome",
            "PositionVCF",
            "ReferenceAlleleVCF",
            "AlternateAlleleVCF",
            "Assembly",
        ],
        inplace=True,
        errors="ignore",
    )

    _validate_annotate_cols(merged)

    return merged


if __name__ == "__main__":
    from config import DEMO_VCF
    from src.vcf_annotator.parsing.vcf_parser import parse_vcf

    vcf_df, meta = parse_vcf(DEMO_VCF)
    clinvar_df = load_clinvar()
    results = annotate(vcf_df, clinvar_df)

    print(f"\n{len(results)} total variants")
    print(f"{results['ClinicalSignificance'].notna().sum()} matched in ClinVar\n")
    print(
        results[
            [
                "CHROM",
                "POS",
                "REF",
                "ALT",
                "ClinicalSignificance",
                "GeneSymbol",
                "PhenotypeList",
                "ClinVar_URL",
            ]
        ].head(20)
    )
