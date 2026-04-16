# VCF-TO-CLINVAR
A drag-and-drop web application for annotating human genetic variants against ClinVar.

![Demo](demo.gif)

**Live App:** https://varclin.streamlit.app/

## Inspiration
No web-based tool exists for finding ClinVar entries associated with variants of clinical significance from a VCF file.
Existing tools for this task require a command-line interface (such as ANNOVAR or VEP), which some researchers, including students, may not be familiar with.

VCF-to-ClinVar fills that gap, providing a simple, easy-to-use tool for finding clinically relevant variants in a VCF file.
Users simply upload a VCF file and instantly see which variants appear in ClinVar, their clinical significance,
associated phenotypes, and links to PubMed articles related to the selected variant.

## Dev Setup

The demo data is included in the repository. To get started,
ensure `pixi` and `just` are installed — see [`INSTALL.md`](INSTALL.md) — then run:

```bash
just install
streamlit run app.py
```

To regenerate the demo data from scratch or work with the full dataset:

```bash
just build-all
```

> **Note:** This project was developed across Linux (linux-64), macOS, and Windows.
> The primary environment manager is pixi — see INSTALL.md for platform-specific setup instructions.


## Using the Web Tool

Once setup is complete, launch the app from the project root:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`, if not opened automatically.

Simply drag a VCF file into the upload box. The app will display all variants found in the ClinVar database in a table along with links to their associated ClinVar pages. Use the dropdown menu to filter variants based on clinical significance.

Below the variant table, users can select a variant and see PubMed articles about that variant, including the abstracts and PubMed links.

## Input Requirements

- Unzipped VCF files (`.vcf`) up to 1 GB
- Single-sample VCFs only (multi-sample support is not currently available)
- VCF must use GRCh38 (hg38) coordinates to match the ClinVar database. Other genome builds may produce incorrect or missing matches

## Interpreting Output

The results table displays only variants matched in ClinVar and includes
the following columns:

- **Chromosome / Position** — genomic location of the variant
- **Alternate Allele** — the variant allele observed in the uploaded VCF
- **Clinical Significance** — ClinVar's classification (e.g. Pathogenic,
  Benign, Uncertain Significance)
- **Gene Symbol** — the gene the variant falls in
- **Phenotype** — associated disease or condition from ClinVar
- **ClinVar Link** — direct link to the variant's ClinVar entry

> **Note:** Variants with no ClinVar match are silently excluded from the results table.

## Team

Northeastern University BioHacks 2026 — MS Bioinformatics

| Name | Email | Role |
|------|-------|------|
| Jeremy Davis | davis.jer@northeastern.edu | VCF parser · ClinVar merge · Streamlit app foundation |
| Trace Lail | lailtrace@gmail.com | Project infrastructure · automated build pipeline (justfile) · test suite with edge case coverage · exception handling and input validation · demo data generation · repository architecture |
| Miguel Trejo Acosta | trejoacosta.m@northeastern.edu | UI polish · color gradients · additional app functionality · Front-end debugging

## Special Thanks

Thank you to Amanda Gale and Charity Acheampong for organizing
Northeastern University BioHacks 2026.

## Future Contributions

We welcome contributions and have several areas identified for future development:

- Support for gzipped VCF files (`.vcf.gz`)
- Multi-sample VCF support
- Expanded genome build support beyond GRCh38
- Full ClinVar database deployment (current demo is scoped to chr21)
- Additional variant annotation sources beyond ClinVar
- Downloadable annotated results as CSV or Excel
