import streamlit as st

pages = [
    st.Page("pages/home.py", title="Home", icon=":material/home:"),
    st.Page("pages/graph.py", title="Graphs", icon=":material/monitoring:"),
    st.Page("pages/todolist.py", title="To-Do List", icon=":material/checklist:")
]

pg = st.navigation(pages, position="sidebar", expanded=True)

pg.run()