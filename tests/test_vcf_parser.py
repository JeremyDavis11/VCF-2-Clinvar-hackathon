import pandas as pd
import pytest

from config import TEST_VCF
from vcf_annotator.parsing.vcf_parser import parse_vcf


@pytest.fixture
def empty_vcf():
    empty_file = """"""
    return empty_file


# Assert the dataframe and column types
def test_parse_vcf():
    df, meta = parse_vcf(TEST_VCF)

    assert isinstance(df, pd.DataFrame)

    assert pd.api.types.is_string_dtype(
        df["CHROM"]
    )  # newer pandas version doesn't accept dtype == "object"
    assert pd.api.types.is_integer_dtype(df["POS"])


# check for empty vcf file
def test_parse_vcf_empty(tmp_path):
    empty_file = tmp_path / "empty.vcf"
    empty_file.write_text("""##fileformat=VCFv4.1
##reference=GRCh38
##source=ClinVar_manually_curated
##INFO=<ID=GENE,Number=1,Type=String,Description="Gene symbol">
##INFO=<ID=CLNSIG,Number=1,Type=String,Description="ClinVar clinical significance">
##INFO=<ID=CLNID,Number=1,Type=Integer,Description="ClinVar VariationID">
##INFO=<ID=DISEASE,Number=1,Type=String,Description="Associated disease">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO""")
    df, meta = parse_vcf(empty_file)
    assert len(df) == 0


# Check for file not found
def test_parse_vcf_not_found():
    with pytest.raises(FileNotFoundError):
        parse_vcf("path/to/nowhere.vcf")
