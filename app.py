import streamlit as st
import pandas as pd
# VCF parsing function
from src.vcf_annotator.parsing.vcf_parser import parse_vcf
# ClinVar annotation and PubMed search functions
from src.vcf_annotator.annotation.clinvar_merge import load_clinvar, annotate
# PubMed search function
from src.vcf_annotator.pubmed_search.search_pubmed import search_pubmed

# cache clinvar data for faster use, with a custom spinner message on first load
@st.cache_data(show_spinner="Loading ClinVar database… (first load only)")
def get_clinvar():
    return load_clinvar()

st.set_page_config(
    page_title="VCF-to-ClinVar Annotator",
    page_icon="🧬",
    layout="wide"
)

st.header("VarClin🧬")

st.markdown("""This tool matches variants from a VCF file against the 
**ClinVar** database to identify clinically significant findings
and provides links to relevant literature. Upload your VCF file to get started!""")
st.divider()

# color coding for clinical significance
def color_significance(val):
    val = val.lower()

    if "benign" in val:
        return "background-color: #09660c;"  # dark green
    elif "pathogenic" in val:
        return "background-color: #ab092c;"  # red
    elif "uncertain" in val:
        return "background-color: #eba52d;"  # orange
    elif "conflicting" in val:
        return "background-color: #e2d6f3;"  # light purple
    else:
        return ""  # no color for other values

    
def main():
    st.title("VCF-to-ClinVar Annotator")
    # set page config with title, icon, and layout
    

    clinvar = get_clinvar() # cached ClinVar DataFrame

    # UI for uploading VCF and displaying results
    st.markdown("Upload a VCF file to identify clinically significant variants from the **ClinVar** database.")

    # file uploader that accepts VCF files, with a custom key to avoid conflicts
    uploaded_file = st.file_uploader("Upload a VCF file or drag and drop it here", type=["vcf"], key="vcf_uploader")

    # use tempfile to save the uploaded file for processing, and os to clean up afterward
    import tempfile
    import os 
    # if a file is uploaded, process it and display results
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".vcf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

         # process the uploaded file
        # st.spinner will show a loading message while the annotation is happening, which can take a few seconds on first load
        try:
            with st.spinner("Annotating VCF against ClinVar..."):
                vcf_df, meta = parse_vcf(tmp_path) # user's uploaded VCF parsed into a DataFrame and metadata
                results = annotate(vcf_df, clinvar) # merged DataFrame with ClinVar annotations added to the user's VCF variants
        finally:
            os.unlink(tmp_path)  # ✅ delete AFTER use

       
        #with st.spinner("Annotating VCF against ClinVar..."):
            #vcf_df, meta = parse_vcf(tmp_path) # user's uploaded VCF
            #results = annotate(vcf_df, clinvar) # merged DataFrame with everything
            #os.unlink(tmp_path) # clean up temp file

    # display summary metrics about the results
        matched = results[results['ClinicalSignificance'].notna()]
        # calculate unmatched count for display
        unmatched_count = len(results) - len(matched)
        col1, col2, col3 = st.columns(3)
        # display metrics in columns
        # the total variants metric shows the total number of variants in the uploaded VCF,
        #  which is the length of the results DataFrame
        col1.metric("Total Variants",    len(results))
        col2.metric("ClinVar Matches",   len(matched))
        col3.metric("No ClinVar Record", unmatched_count)

        # Filter variants by clinical significance with a drop down menu
        sig_filter = st.selectbox("Filter by Clinical Significance", ["ALL"] + sorted(matched["ClinicalSignificance"].dropna().unique().tolist()))
        if sig_filter != "ALL":
            matched = matched[matched["ClinicalSignificance"] == sig_filter]



        # define columns to display in the table, including a link column for ClinVar URLs
        display_cols = ["CHROM", 
                "POS", 
                # the REF and ALT columns show the reference and alternate alleles for each variant, which are essential for understanding the specific genetic change being annotated
                "REF",
                "ALT", 
                "ClinicalSignificance",
                "GeneSymbol",
                "PhenotypeList",
                "ClinVar_URL"]
        # allow users to download results as CSV, with only the display columns included in the download
        csv = matched[display_cols].to_csv(index=False).encode()
        st.download_button("⬇ Download results as CSV", csv, "clinvar_results.csv", "text/csv")
        
        

    # display variant table
        # the column_config option allows us to specify that the ClinVar_URL column should be 
        # rendered as clickable links with the label "ClinVar Link"
       # st.dataframe(matched[display_cols], 
                    # column_config={"ClinVar_URL": st.column_config.LinkColumn("ClinVar Link")})

    # apply color coding to the ClinicalSignificance column using the color_significance function, 
    # and then display the styled dataframe with the link column configuration
        styled_df = matched[display_cols].style.map(
        color_significance, subset=["ClinicalSignificance"]
    )

# display the styled dataframe with the link column configuration
        st.dataframe(
        styled_df,
        column_config={"ClinVar_URL": st.column_config.LinkColumn("ClinVar Link")}
    )        


    # grab gene symbols for lit lookup
        # the gene symbol is important for the PubMed search because it allows us to search
        #  for literature related to the specific gene associated with the variant, which can provide insights into the clinical significance and potential implications of the variant.
        if matched.empty:
            st.warning("No matched variants to search literature for.")
        else:
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

