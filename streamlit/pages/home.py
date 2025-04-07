import streamlit as st

def home():
    st.title("Streamlit Stock Market App")
    st.subheader("A simple app to display stock market data")
    
    st.write("This app allows you to view market data for various stock instruments.")
    st.write("Navigate between different pages using the sidebar.")

home()