import streamlit as st

st.set_page_config(page_title="Acknowledgement", layout="wide")

# Top Header with Logos and Title
col1, col2, col3 = st.columns([1.5, 20, 2])

with col1:
    st.image("static/images/icarlogo.png", width=120)

with col2:
    st.markdown(
        "<h2 style='text-align:center;'>BENLiP: Bagging based Ensemble Model to Identify Nucleosome and Linker Positioning</h2>",
        unsafe_allow_html=True
    )

with col3:
    st.image("static/images/iasri-logo.png", width=120)

st.markdown("---")

# Acknowledgement Title
st.markdown("<h1 style='text-align:center;'>Acknowledgement</h1>", unsafe_allow_html=True)

st.markdown("---")

# Acknowledgement Content
st.markdown("""
<div style='text-align:center; font-size:18px;'>

The authors gratefully acknowledge the financial support provided by the <b>Department of Biotechnology (DBT), Government of India, New Delhi</b>, under the project <b>No. BT/PR40191/BTIS/137/82/2023</b>.

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown(
    "<div style='background-color:#32CD32; text-align:center'>"
    "<p style='color:white'>© 2025 ICAR-Indian Agricultural Statistics Research Institute, New Delhi-110012</p>"
    "</div>",
    unsafe_allow_html=True
)
