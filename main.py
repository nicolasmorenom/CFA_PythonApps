import streamlit as st
import plotly.express as px
from fsa_analyzer import get_financials, calculate_ratios

st.set_page_config(page_title="CFA L1 Financial Statement Analyzer", layout="wide")
st.title("CFA Level 1 – Financial Statement Analysis Dashboard")

ticker = st.text_input("Enter ticker (e.g. AAPL, MSFT)", "AAPL").upper()

if st.button("Analyze"):
    with st.spinner("Downloading data..."):
        bs, inc, cf = get_financials(ticker)
        ratios = calculate_ratios(bs, inc, cf)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Key Ratios")
        st.dataframe(ratios, use_container_width=True)

    with col2:
        st.subheader("Credit & Distress")
        z = ratios['Altman Z-Score']
        st.metric("Altman Z-Score", f"{z:.2f}")
        if z > 2.99:
            st.success("Safe Zone")
        elif z > 1.81:
            st.warning("Grey Zone")
        else:
            st.error("Distress Zone")
