import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="hellofasting",
    page_icon="😈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

apple_css = """
<style>
    :root {
        color-scheme: light;
    }

    html, body, .stApp {
        background-color: white !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: black !important;
    }

    header, footer, .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    h1 {
        font-weight: 700 !important;
        color: black !important;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px !important;
        background-color: rgb(0, 113, 227) !important;
        color: white !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 14px !important;
        font-size: 16px !important;
    }
    
    .stButton > button:hover {
        background-color: rgb(0, 122, 255) !important;
    }

    .big-timer {
        font-size: 72px;
        font-weight: 600;
        text-align: center;
        font-feature-settings: "tnum";
        font-variant-numeric: tabular-nums;
        color: black;
        margin-top: 30px;
        margin-bottom: 20px;
