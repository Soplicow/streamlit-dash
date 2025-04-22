import streamlit as st
import pandas as pd
import numpy as np

# Streamlit Reference Guide
st.title("Streamlit Reference Guide")

# Displaying Text
st.header("Displaying Text")
st.subheader("Basic Text Functions")
st.code("""
st.title("Title")
st.header("Header")
st.subheader("Subheader")
st.text("Simple text")
st.markdown("Markdown text")
st.latex(r"e^{i\pi} + 1 = 0")
""")
st.title("Title Example")
st.header("Header Example")
st.subheader("Subheader Example")
st.text("This is simple text.")
st.markdown("**Markdown Example**: _italic_, **bold**, `code`")
st.latex(r"e^{i\pi} + 1 = 0")

# Displaying Data
st.header("Displaying Data")
st.subheader("DataFrame and Charts")
data = pd.DataFrame(np.random.randn(10, 3), columns=["A", "B", "C"])
st.code("""
st.dataframe(data)
st.table(data)
st.line_chart(data)
st.bar_chart(data)
st.area_chart(data)
""")
st.dataframe(data)
st.line_chart(data)

# User Input
st.header("User Input")
st.subheader("Input Widgets")
st.code("""
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=0, max_value=120)
agree = st.checkbox("I agree")
color = st.selectbox("Pick a color:", ["Red", "Green", "Blue"])
""")
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=0, max_value=120)
agree = st.checkbox("I agree")
color = st.selectbox("Pick a color:", ["Red", "Green", "Blue"])

# Layouts
st.header("Layouts")
st.subheader("Columns and Expander")
st.code("""
col1, col2 = st.columns(2)
with col1:
    st.write("Column 1")
with col2:
    st.write("Column 2")

with st.expander("See more"):
    st.write("Expanded content")
""")
col1, col2 = st.columns(2)
with col1:
    st.write("Column 1")
with col2:
    st.write("Column 2")

with st.expander("See more"):
    st.write("Expanded content")

# Media
st.header("Media")
st.subheader("Images and Videos")
st.code("""
st.image("https://via.placeholder.com/150", caption="Sample Image")
st.video("https://www.youtube.com/watch?v=5qap5aO4i9A")
""")
st.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fdesignshack.net%2Fwp-content%2Fuploads%2Fplacehold.jpg&f=1&nofb=1&ipt=3fb9596498815c2b7af5b5c664125e15b4d63115c0ecb1545e5030b11dd78dd6", caption="Sample Image")
st.video("https://www.youtube.com/watch?v=5qap5aO4i9A")

# Conclusion
st.header("Conclusion")
st.markdown("""
This guide covers the basics of Streamlit. For more details, visit the [Streamlit Documentation](https://docs.streamlit.io/).
""")