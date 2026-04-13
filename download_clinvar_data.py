"""
Download and trim ClinVar variant summary data for use with the VCF annotation dashboard.
Run this once before using the main annotation script.
"""

import pandas as pd
import urllib.request
import os

URL = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz'
RAW_FILE = 'variant_summary.txt.gz'
TRIMMED_FILE = 'clinvar_trimmed.csv'

if os.path.exists(TRIMMED_FILE):
    print(f'{TRIMMED_FILE} already exists. Delete it to re-download.')
else:
    print('Downloading ClinVar variant summary (this may take a few minutes)...')
    urllib.request.urlretrieve(URL, RAW_FILE)
    print('Download complete. Processing...')

    clinvar = pd.read_csv(RAW_FILE, sep='\t', compression='gzip', low_memory=False)
    clinvar = clinvar[clinvar['Assembly'] == 'GRCh38']
    clinvar = clinvar[['Chromosome', 'PositionVCF', 'ReferenceAlleleVCF', 'AlternateAlleleVCF',
                       'ClinicalSignificance', 'GeneSymbol', 'PhenotypeList', 'ReviewStatus', 'VariationID']]
    clinvar.to_csv(TRIMMED_FILE, index=False)

    # clean up the large raw file
    os.remove(RAW_FILE)

    print(f'Saved {len(clinvar)} GRCh38 variants to {TRIMMED_FILE}')
