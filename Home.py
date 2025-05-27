import streamlit as st

st.set_page_config( page_title="BENLiP", initial_sidebar_state="expanded", layout="wide")
col1, col2, col3 = st.columns([1.5, 20, 2])

with col1:
    st.image("static/images/icarlogo.png", width=200)

with col2:
    st.markdown("<h1 style='text-align:center;'> BENLiP: Bagging based Ensemble model to identify Nucleosome and Linker Positioning</h1>", unsafe_allow_html=True)

with col3:
    st.image("static/images/iasri-logo.png", width=200)

st.markdown("---")
st.text("")

col1_1, col2_1 = st.columns([1, 2])

with col1_1:
    st.header("Background")
    st.markdown(
        """
        <div style='text-align: justify;'>
            Nucleosome Positioning is the specific positioning of nucleosomes on the DNA sequence. 
            Nucleosomes are chromatin structural units made up of DNA coiled around histone proteins. 
            Their positioning is important in the regulation of gene expression, DNA replication, and repair 
            by determining the accessibility of DNA to transcription factors and other regulatory proteins.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.header("About BENLiP")
    st.markdown(
        """
        <div style='text-align: justify;'>
            BENLiP employs a bagging-based ensemble model for nucleosome positioning. 
            BENLiP helps to differentiate the nucleosome and linker sequences for 
            <i>Homo sapiens</i>, <i>Caenorhabditis elegans</i>, <i>Drosophila melanogaster</i>, 
            and <i>Saccharomyces cerevisiae</i>.
        </div>
        """,
        unsafe_allow_html=True
    )
with col2_1:
    st.image("static/images/Workflow.jpg")

st.text("")
st.markdown("<div style='background-color:#32CD32; text-align:center'><p style='color:white'>Copyright © 2025 ICAR-Indian Agricultural Statistics Research Institute, New Delhi-110012. All rights reserved.</p></div>", unsafe_allow_html=True)
