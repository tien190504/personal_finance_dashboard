import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Personal Finance Risk Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🏦 Personal Finance Risk Dashboard")

st.markdown("""
### Welcome to your Risk Dashboard
Select an asset class from the sidebar to begin analyzing your investment potential.

This tool helps you understand the **relationship between risk, time, and returns** across different financial instruments.

#### Available Asset Classes:
- **💰 Savings**: Low risk, steady growth.
- **📜 Bonds**: Balanced income and safety.
- **📈 Index Funds**: Market-linked growth.
- **₿ Crypto**: High volatility, high potential reward.

---
*Built with Python & Streamlit*
""")

# Sidebar Navigation Info
st.sidebar.success("Select a page above 👆")
st.sidebar.info("Data usage: All calculations are performed locally in your browser session.")
