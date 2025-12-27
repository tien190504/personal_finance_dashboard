import streamlit as st
from components.dashboard import render_dashboard

st.set_page_config(page_title="Savings | Risk Dashboard", page_icon="💰")
render_dashboard("Savings")
