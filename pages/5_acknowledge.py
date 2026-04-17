import streamlit as st

st.set_page_config(page_title="Acknowledgement", layout="wide")

# Title
st.markdown("<h1 style='text-align:center;'>Acknowledgement</h1>", unsafe_allow_html=True)
st.markdown("---")

# Acknowledgement text
st.markdown("""
The authors gratefully acknowledge the financial support provided by the **Department of Biotechnology (DBT), Government of India, New Delhi**,  
under the project **No. BT/PR40191/BTIS/137/82/2023**.
""")

st.markdown("---")

# Footer
st.markdown(
    "<div style='background-color:#32CD32; text-align:center'>"
    "<p style='color:white'>© 2025 ICAR-Indian Agricultural Statistics Research Institute, New Delhi-110012</p>"
    "</div>",
    unsafe_allow_html=True
)