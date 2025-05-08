import streamlit as st

def home():
    st.title("Streamlit Data Dashboard")
    st.subheader("A simple app to display stock market data, charts, and more.")
    
    st.write("This app allows you to view and analyze various datasets, including stock market data, meteorite landings, and a todo list.")
    st.write("Navigate between different pages using the sidebar.")

home()