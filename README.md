# VCF-TO-CLINVAR
A web-based application for determining clinically significant variants from a human VCF file.

## Justification
No web-based tool exists for finding ClinVar entries associated with variants of clinical significance from a VCF file. Existing tools for this task require a command line interface, which some researchers, including students, may not be familiar with. This tool addresses that gap and provides a simple, easy to use tool for finding variants of clinical relevance in a VCF file. The application also includes exploratory features such as filtering by clinical relevance and links to PubMed articles related to the selected variant.

## Set Up
Setup instructions found in `INSTALL.md`

To launch the web app for testing use `streamlit run app.py` from the project's main directory.


## Using the Web Tool
Simply drag a VCF file into the upload box. The website will display all variants found in the ClinVar database in a table along with links to their associated ClinVar pages. Use the dropdown menu to filter variants based on clinical significance.

Below the variant table, users can select a variant and see PubMed articles about that variant, including the abstracts and PubMed links. 

## Input Requirements

- Unzipped VCF files (`.vcf`) up to 2 GB
- VCF must use GRCh38 (hg38) coordinates to match the ClinVar database. Other genome builds may produce incorrect or missing matches

## Interpreting output
The results table displays matched variants with the following columns: Chromosome, Position, Alternate Allele, Clinical Significance, Gene Symbol, Phenotype, and a link to the ClinVar entry.

![Demo](demo.gif)

## Team Members
Jeremy Davis | MS Bioinformatics, Northeastern University | davis.jer@northeastern.edu

## Special Thanks
Thank you to Amanda Gale and Charity Acheampong for organizing Northeastern University BioHacks 2026
