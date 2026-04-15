# BIOHACK 2026 — justfile
# Run `just` to see available commands

# ── Variables ─────────────────────────────────────────────────────────────────

DATA_RAW       := "data/raw"
DATA_DEMO      := "data/demo"
DATA_PROCESSED := "data/processed"
DATA_TEST      := "data/test"

CLINVAR_URL := "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
CLINVAR_GZ  := DATA_RAW / "variant_summary.txt.gz"
CLINVAR_TXT := DATA_RAW / "variant_summary.txt"

VCF_URL  := "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/release/20190312_biallelic_SNV_and_INDEL/ALL.chr21.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz"
VCF_GZ   := DATA_RAW / "ALL.chr21.GRCh38.phased.vcf.gz"
VCF_FILE := DATA_RAW / "ALL.chr21.GRCh38.phased.vcf"

# ── Default: list all recipes ─────────────────────────────────────────────────

default:
    @just --list

# ── Environment ───────────────────────────────────────────────────────────────

# Install Python dependencies
install:
    pixi add python pandas streamlit plotly pytest ruff mypy

# Run once after cloning — sets up dirs and installs everything
setup: init install

# Run tests
test:
    pixi run pytest tests/

# Lint
lint:
    pixi run ruff check .

# Typecheck
typecheck:
    pixi run mypy src/

# Run all checks — useful before committing
check: lint typecheck test

# ── Setup ─────────────────────────────────────────────────────────────────────

# Create all required data directories
init:
    mkdir -p {{DATA_RAW}}
    mkdir -p {{DATA_DEMO}}
    mkdir -p {{DATA_PROCESSED}}
    mkdir -p {{DATA_TEST}}

# ── Download ──────────────────────────────────────────────────────────────────

# Download both ClinVar and the 1000 Genomes chr21 VCF (GRCh38)
download: init download-clinvar download-vcf

# Download ClinVar variant_summary.txt.gz, decompress, and preview
download-clinvar: init
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

# Download 1000 Genomes chr21 VCF (GRCh38, biallelic SNV+INDEL), decompress, and preview
download-vcf: init
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

# ── Inspect ───────────────────────────────────────────────────────────────────

# Show the column headers of the ClinVar TSV
clinvar-columns:
    @echo "━━━ ClinVar columns ━━━"
    head -n 1 {{CLINVAR_TXT}} | tr '\t' '\n' | nl

# Count variants in the VCF (excludes header lines)
vcf-count:
    @echo "━━━ Variant count in chr21 VCF ━━━"
    grep -vc "^#" {{VCF_FILE}}

# ── Data Pipeline ─────────────────────────────────────────────────────────────

# Stream ClinVar and filter to GRCh38 chr21 only → data/demo/clinvar_chr21.tsv
filter-clinvar-chr21:
    pixi run python scripts/clinvar_filter_chr21.py

# Stratified subsample — every 50th variant → data/processed/chr21_subsampled.vcf
subsample-vcf:
    pixi run python scripts/vcf_subsample.py \
        --input  {{VCF_FILE}} \
        --output data/processed/chr21_subsampled.vcf \
        --n 50

# Filter subsampled VCF to ClinVar-matched variants only → data/demo/demo.vcf
filter-clinvar:
    pixi run python scripts/vcf_clinvar_filter.py \
        --input  data/processed/chr21_subsampled.vcf \
        --output data/demo/demo.vcf

# Append known pathogenic variants to subsampled VCF → data/processed/chr21_with_pathogenic.vcf
append-pathogenic:
    grep "^#"  data/processed/chr21_subsampled.vcf  > data/processed/chr21_with_pathogenic.vcf
    grep -v "^#" data/processed/chr21_subsampled.vcf >> data/processed/chr21_with_pathogenic.vcf
    grep -v "^#" data/test/known_pathogenic_chr21.vcf >> data/processed/chr21_with_pathogenic.vcf
    @echo "✓ Written to data/processed/chr21_with_pathogenic.vcf"

# Build demo VCF — full pipeline in sequence
build-demo: filter-clinvar-chr21 subsample-vcf filter-clinvar
    @echo "✓ demo.vcf ready at data/demo/demo.vcf"

# Full setup from scratch — for new teammates
build-all: init install download build-demo
    @echo "✓ Environment, data, and demo files ready"

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
    rm -rf data/
    @echo "✓ data/ directory removed"
