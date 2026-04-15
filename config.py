from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

# Directories
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_DEMO = PROJECT_ROOT / "data" / "demo"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_TEST = PROJECT_ROOT / "data" / "test"

# Intermediate files
SUBSAMPLED_VCF = DATA_PROCESSED / "chr21_subsampled.vcf"
SUBSAMPLED_PATHOGENIC = DATA_PROCESSED / "chr21_with_pathogenic.vcf"

# Streamlit demo files
CLINVAR_PATH = DATA_DEMO / "clinvar_chr21.tsv"
DEMO_VCF = DATA_DEMO / "demo.vcf"
