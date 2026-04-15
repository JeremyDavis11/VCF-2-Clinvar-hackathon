import io
import time
import gzip
import pandas as pd
import streamlit as st

# ════════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be first Streamlit call)
# ════════════════════════════════════════════════════════════════════════════════
# set page config:  tells Streamlit how the app page should behave and appear.
st.set_page_config(
    page_title="VarSight · ClinVar Annotator",
    page_icon="🧬",
    layout="wide",
    # This sets the sidebar to be collapsed by default when the app opens.
    initial_sidebar_state="collapsed",


)
