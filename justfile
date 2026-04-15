# BIOHACK 2026 — justfile
# Run `just` to see available commands

# ── Variables ────────────────────────────────────────────────────────────────

DATA_DIR := "data/raw"

CLINVAR_URL := "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
CLINVAR_GZ  := DATA_DIR / "variant_summary.txt.gz"
CLINVAR_TXT := DATA_DIR / "variant_summary.txt"

VCF_URL := "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/release/20190312_biallelic_SNV_and_INDEL/ALL.chr21.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz"
VCF_GZ  := DATA_DIR / "ALL.chr21.GRCh38.phased.vcf.gz"
VCF_FILE := DATA_DIR / "ALL.chr21.GRCh38.phased.vcf"

# ── Default: list all recipes ─────────────────────────────────────────────────

default:
    @just --list

# ── Environment ───────────────────────────────────────────────────────────────

# Install Python dependencies
install:
    pixi add python pandas streamlit plotly


# ── Setup ─────────────────────────────────────────────────────────────────────

# Create the data directory if it doesn't exist
setup:
    mkdir -p {{DATA_DIR}}

# ── Download ──────────────────────────────────────────────────────────────────

# Download, unzip, and preview both ClinVar and the 1000 Genomes chr21 VCF (GRCh38)
download: setup download-clinvar download-vcf

# Download ClinVar variant_summary.txt.gz, decompress, and show first 10 lines
download-clinvar: setup
    @echo "━━━ Downloading ClinVar variant_summary.txt.gz ━━━"
    curl -L --progress-bar -o {{CLINVAR_GZ}} {{CLINVAR_URL}}
    @echo ""
    @echo "━━━ Decompressing ClinVar ━━━"
    gunzip -k -f {{CLINVAR_GZ}}
    @echo ""
    @echo "━━━ ClinVar — first 10 lines ━━━"
    head -n 10 {{CLINVAR_TXT}}
    @echo ""
    @echo "✓ ClinVar saved to {{CLINVAR_TXT}}"

# Download 1000 Genomes chr21 VCF (GRCh38, biallelic SNV+INDEL), decompress, and show first 10 variant lines
download-vcf: setup
    @echo "━━━ Downloading 1000 Genomes chr21 VCF (GRCh38) ━━━"
    curl -L --progress-bar -o {{VCF_GZ}} {{VCF_URL}}
    @echo ""
    @echo "━━━ Decompressing VCF ━━━"
    gunzip -k -f {{VCF_GZ}}
    @echo ""
    @echo "━━━ 1000 Genomes chr21 VCF — first 10 variant lines (skipping headers) ━━━"
    grep -v "^#" {{VCF_FILE}} | head -n 10
    @echo ""
    @echo "✓ VCF saved to {{VCF_FILE}}"

# ── Inspect (safe to run anytime) ─────────────────────────────────────────────

# Show the column headers of the ClinVar TSV
clinvar-columns:
    @echo "━━━ ClinVar columns ━━━"
    head -n 1 {{CLINVAR_TXT}} | tr '\t' '\n' | nl

# Count variants in the VCF (excludes header lines)
vcf-count:
    @echo "━━━ Variant count in chr21 VCF ━━━"
    grep -vc "^#" {{VCF_FILE}}

# ── Demo Data Preparation ─────────────────────────────────────────────────────

# Stratified subsample — every 100th variant across the full chr21 VCF
subsample-vcf:
    pixi run python scripts/vcf_subsample.py \
        --input data/raw/ALL.chr21.GRCh38.phased.vcf \
        --output data/demo/chr21_subsampled.vcf \
        --n 50

# Pre-filter ClinVar to chr21 only (run once, saves RAM downstream)
filter-clinvar-chr21:
    pixi run python scripts/clinvar_filter_chr21.py

# Filter subsampled VCF to ClinVar-matched variants only
filter-clinvar:
    pixi run python scripts/vcf_clinvar_filter.py \
        --input data/demo/chr21_subsampled.vcf \
        --output data/demo/demo.vcf


# Run both in sequence to build the final demo VCF
build-demo: subsample-vcf filter-clinvar-chr21 filter-clinvar
    @echo "✓ demo.vcf ready at data/demo/demo.vcf"

# ── Execution ─────────────────────────────────────────────────────────────────

# Run the VCF parser test
run-parser:
    pixi run python src/vcf_annotator/parsing/vcf_parser.py

# ── Clean ─────────────────────────────────────────────────────────────────────

# Remove decompressed files only (keep the .gz archives)
clean:
    rm -f {{CLINVAR_TXT}} {{VCF_FILE}}
    @echo "✓ Decompressed files removed (archives kept)"

# Remove everything in data/
clean-all:
    rm -rf {{DATA_DIR}}
    @echo "✓ data/ directory removed"
