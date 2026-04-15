from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_DEMO = PROJECT_ROOT / "data" / "demo"
DATA_TEST = PROJECT_ROOT / "data" / "test"

CLINVAR_PATH = DATA_DEMO / "clinvar_chr21.tsv"
DEMO_VCF = DATA_DEMO / "chr21_subsampled.vcf"
