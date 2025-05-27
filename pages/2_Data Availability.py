import streamlit as st
import io

st.set_page_config( page_title="BENLiP", initial_sidebar_state="expanded", layout="wide")
col1, col2, col3 = st.columns([1.5, 20, 2])

with col1:
    st.image("static/images/icarlogo.png", width=150)

with col2:
    st.markdown("<h1 style='text-align:center;'> BENLiP: Bagging based Ensemble model to identify Nucleosome and Linker Positioning</h1>", unsafe_allow_html=True)

with col3:
    st.image("static/images/iasri-logo.png", width=150)

st.markdown("---")
st.text("")

with open("static/data/nucleosomes_vs_linkers.fasta", "rb") as f:
    
    st.markdown("**Sample Preview:**")
    st.text(f.readline().decode('UTF-8'))
    st.text(f.readline().decode('UTF-8'))
    st.write(f.readline().decode('UTF-8'))
    st.write(f.readline().decode('UTF-8'))

    
    st.download_button("Download Sample File", f, file_name="nucleosomes_vs_linkers.fasta", icon=":material/download:")

st.text("")
st.text("")
st.text("")
st.markdown("<div style='background-color:#32CD32; text-align:center'><p style='color:white'>Copyright © 2025 ICAR-Indian Agricultural Statistics Research Institute, New Delhi-110012. All rights reserved.</p></div>", unsafe_allow_html=True)