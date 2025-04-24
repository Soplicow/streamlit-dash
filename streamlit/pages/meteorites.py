import streamlit as st
import pandas as pd

@st.cache_data
def from_data_file(filename):
    """Load data from a CSV file and return it as a DataFrame."""
    return pd.read_csv(filename)

