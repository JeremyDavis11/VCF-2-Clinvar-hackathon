import pandas as pd

from config import TEST_VCF
from src.vcf_annotator.parsing.vcf_parser import parse_vcf


def test_parse_vcf():
    df, meta = parse_vcf(TEST_VCF)

    assert isinstance(df, pd.DataFrame)
