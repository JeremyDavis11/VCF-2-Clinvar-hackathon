import pandas as pd

from config import CLINVAR_PATH


def load_clinvar(path=CLINVAR_PATH):
    """
    Load and preprocess the ClinVar variant summary TSV.

    Args:
        path: Path to variant_summary.txt (str or Path)

    Returns:
        DataFrame with relevant ClinVar columns, filtered to GRCh38 assembly
    """
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
