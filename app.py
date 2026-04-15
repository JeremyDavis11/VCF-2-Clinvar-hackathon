import io
import time
import gzip
import pandas as pd
import streamlit as st

# ════════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be first Streamlit call)
# ════════════════════════════════════════════════════════════════════════════════
# set page config:  tells Streamlit how the app page should behave and appear.
st.header("VarSight")
st.subheader("The ClinVar Annotator for non-coders")
st.set_page_config(
    page_title="VarSight · ClinVar Annotator",
    page_icon="🧬",
    layout="wide",
    # This sets the sidebar to be collapsed by default when the app opens.
    initial_sidebar_state="collapsed",


)

st.title("VarSight")

# upload card, which is the container for the file uploader and analyze button
uploaded_file = st.file_uploader("Upload a VCF file", type=["vcf","tsv"], key="file_uploader")
if uploaded_file:
    st.success("File uploaded successfully")
else:
    st.warning("Please upload a VCF file to proceed")
st.button("Analyze")
#-----------------------------------------------------------------------------------------

# <style> tag allows us to write custom CSS to style the Streamlit app. Here, we are importing two fonts from Google Fonts (DM Sans and DM Mono) and applying them to the entire app.
#  We are also setting a background color and text color for the app.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
 
<! -- Comments: applies rest to all elements, allows for custom styling for browser compatibility -->
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
 
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #f7f6f2;
    color: #f5182f; 
}
            
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }
                         
            
}
            
""", unsafe_allow_html=True)
# unsafe_allow_html=True allows us to include raw HTML in our Streamlit app, 
# which is necessary for the custom styling we are applying.

