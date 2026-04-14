import pandas as pd

clinvar = pd.read_csv('clinvar_trimmed.csv')

def parse_vcf(filepath):
    meta = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('##'):
                meta.append(line)
            elif line.startswith('#CHROM'):
                cols = line.strip().lstrip('#').split('\t')
                break
        df = pd.read_csv(f, sep='\t', names=cols)
    return df, meta


#
vcf_df, meta = parse_vcf('test_real.vcf')

# make CHROM a string to match ClinVar
vcf_df['CHROM'] = vcf_df['CHROM'].astype(str)

# merge
results = pd.merge(
    vcf_df,
    clinvar,
    left_on=['CHROM', 'POS', 'REF', 'ALT'],
    right_on=['Chromosome', 'PositionVCF', 'ReferenceAlleleVCF', 'AlternateAlleleVCF'],
    how='inner'
)

print(results[['CHROM', 'POS', 'REF', 'ALT', 'ClinicalSignificance', 'GeneSymbol', 'PhenotypeList']])