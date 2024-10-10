import streamlit as st

def configure_streamlit():
    st.set_page_config(
        page_title="Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"

    )

# style_config.py

def apply_custom_css():
    st.markdown("""
    <style>

    /* Change the style of the selectbox and date_input widgets */
    .stSelectbox, .stDateInput {
        background-color: lightblue;  /* Background color */
        color: black;  /* Text color */
        border: 1px solid #333333 !important;  /* Border color */
        border-radius: 12px;  /* Border radius */
        padding: 5px !important;  /* Padding */
    }

    /* Change the label color of the selectbox and date_input widgets */
    .stSelectbox label, .stDateInput label {
        color: black;  /* Label text color */
    }

    /* Style for the sidebar header */
    .css-2trqyj {
        color: #333333 !important;  /* Header text color */
    }
    </style>
    """, unsafe_allow_html=True)