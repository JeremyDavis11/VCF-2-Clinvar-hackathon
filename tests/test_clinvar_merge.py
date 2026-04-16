import pandas as pd
import pytest

from vcf_annotator.annotation.clinvar_merge import (
    ANNOTATED_COLS,
    _validate_annotate_cols,
    annotate,
    load_clinvar,
)
from vcf_annotator.parsing.vcf_parser import parse_vcf

MISSING_ANNOTATED_COLS = [
    "CHROM",
    "POS",
    "REF",
    "ALT",
    "ClinicalSignificance",
    "PhenotypeList",
]


@pytest.fixture
def simple_vcf(tmp_path):
    vcf = tmp_path / "simple.vcf"
    vcf.write_text("""##fileformat=VCFv4.1
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	100	.	A	T	.	PASS	.""")
    df, _ = parse_vcf(vcf)
    return df


# Validation tests


# Test annotate column validation - has all columns
def test_validate_annotate_cols():
    df = pd.DataFrame(columns=ANNOTATED_COLS)
    _validate_annotate_cols(df)  # should not raise an error


# Test annotate column validation - missing columns
def test_validate_annotate_cols_missing_cols():
    df = pd.DataFrame(columns=MISSING_ANNOTATED_COLS)
    with pytest.raises(ValueError):
        _validate_annotate_cols(df)


# load_clinvar tests


def test_load_clinvar_returns_dataframe():
    df = load_clinvar()
    assert isinstance(df, pd.DataFrame)


def test_load_clinvar_not_empty():
    df = load_clinvar()
    assert len(df) > 0


def test_load_clinvar_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_clinvar("path/to/nowhere.tsv")


# Annotate tests


def test_annotate_returns_dataframe(simple_vcf):
    clinvar_df = load_clinvar()
    result = annotate(simple_vcf, clinvar_df)
    assert isinstance(result, pd.DataFrame)


def test_annotate_output_columns(simple_vcf):
    clinvar_df = load_clinvar()
    result = annotate(simple_vcf, clinvar_df)
    for col in ANNOTATED_COLS:
        assert col in result.columns, f"Missing expected column: {col}"


def test_annotate_empty_vcf():
    vcf_df = pd.DataFrame(
        columns=["CHROM", "POS", "REF", "ALT", "ID", "QUAL", "FILTER", "INFO"]
    )
    clinvar_df = load_clinvar()
    result = annotate(vcf_df, clinvar_df)
    assert len(result) == 0


def test_annotate_clinvar_url_with_valid_id(simple_vcf):
    clinvar_df = pd.DataFrame(
        {
            "Chromosome": ["1"],
            "PositionVCF": [100],
            "ReferenceAlleleVCF": ["A"],
            "AlternateAlleleVCF": ["T"],
            "ClinicalSignificance": ["Pathogenic"],
            "GeneSymbol": ["BRCA1"],
            "PhenotypeList": ["Breast cancer"],
            "Assembly": ["GRCh38"],
            "VariationID": [12345],
        }
    )
    result = annotate(simple_vcf, clinvar_df)
    assert (
        result["ClinVar_URL"].iloc[0]
        == "https://www.ncbi.nlm.nih.gov/clinvar/variation/12345/"
    )


def test_annotate_clinvar_url_with_no_match():
    vcf_df = pd.DataFrame(
        {
            "CHROM": ["1"],
            "POS": [999999999],
            "REF": ["A"],
            "ALT": ["T"],
            "ID": ["."],
            "QUAL": ["."],
            "FILTER": ["PASS"],
            "INFO": ["."],
        }
    )
    clinvar_df = load_clinvar()
    result = annotate(vcf_df, clinvar_df)
    assert result["ClinVar_URL"].iloc[0] is None
