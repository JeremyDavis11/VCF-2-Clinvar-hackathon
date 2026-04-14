from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_DEMO = PROJECT_ROOT / "data" / "demo"

CLINVAR_PATH = DATA_RAW / "variant_summary.txt"
DEMO_VCF = DATA_DEMO / "test_real.vcf"
