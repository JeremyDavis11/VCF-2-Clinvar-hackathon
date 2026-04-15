import streamlit as st
import pandas as pd
from src.vcf_annotator.parsing.vcf_parser import parse_vcf
from src.vcf_annotator.annotation.clinvar_merge import load_clinvar, annotate
from src.vcf_annotator.pubmed_search.search_pubmed import search_pubmed

# cache clinvar data for faster use
@st.cache_data
def get_clinvar():
    return load_clinvar()

def main():
    st.title("VCF-to-ClinVar Annotator")

    clinvar = get_clinvar() # cached ClinVar DataFrame

    uploaded_file = st.file_uploader("Upload a VCF file", type=["vcf"])

    if uploaded_file:
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix=".vcf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        # process the uploaded file
        with st.spinner("Annotating VCF against ClinVar..."):
            vcf_df, meta = parse_vcf(tmp_path) # user's uploaded VCF
            results = annotate(vcf_df, clinvar) # merged DataFrame with everything
            os.unlink(tmp_path) # clean up temp file

        matched = results[results['ClinicalSignificance'].notna()]

        # Filter variants by clinical significance with a drop down menu
        sig_filter = st.selectbox("Filter by Clinical Significance", ["ALL"] + sorted(matched["ClinicalSignificance"].dropna().unique().tolist()))
        if sig_filter != "ALL":
            matched = matched[matched["ClinicalSignificance"] == sig_filter]

        display_cols = ["CHROM", 
                "POS", 
                "ALT", 
                "ClinicalSignificance",
                "GeneSymbol",
                "PhenotypeList",
                "ClinVar_URL"]
        
        # display variant table
        st.dataframe(matched[display_cols], 
                     column_config={"ClinVar_URL": st.column_config.LinkColumn("ClinVar Link")})
        
        # grab gene symbols for lit lookup
        variant_options = matched[display_cols].apply(
            lambda row: f"{row['GeneSymbol']} - {row['CHROM']}:{row['POS']} {row['ALT']}", axis=1
        )

        # literature lookup
        selected = st.selectbox("Select a variant for literature search", variant_options)
        if st.button("Search PubMed"):
            idx = variant_options[variant_options == selected].index[0]
            gene = matched.loc[idx, "GeneSymbol"]
            pmids, abstracts = search_pubmed(gene)
        
            # split abstracts by double newline
            articles = [a.strip() for a in abstracts.split("\n\n\n") if a.strip()]

            # put each article in its own collapseable box on the page
            for i, (pmid, article) in enumerate(zip(pmids, articles)):
                with st.expander(f"article {i + 1} - PMID: {pmid}"):
                    st.write(article)
                    st.markdown(f"[View on Pubmed](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)")

    else:
        st.info("Upload a VCF file to get started")


if __name__ == "__main__":
    main()

