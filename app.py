import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Streamlit App
st.set_page_config(page_title="page analysis tool", layout="wide")
st.title("☁️ page analysis tool- Vikash Goyal")

# How it works section
st.markdown("""
### ℹ️ How it works
1. Enter or paste your text into the text area **OR** upload a `.txt` file.
2. The app will process the text and generate a **Word Cloud**.
3. Words appearing more frequently in your text will appear larger in the cloud.
4. You can use this to visualize themes, keywords, or dominant topics in your data.
""")

# Text input
st.subheader("Enter text")
text_input = st.text_area("Paste your text here", height=200)

# File uploader
st.subheader("Or upload a text file")
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

text = ""
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
elif text_input.strip() != "":
    text = text_input

# Generate word cloud
if text:
    st.subheader("Generated Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.info("Please enter text or upload a file to generate a word cloud.")

# Footer
st.markdown("""
---
👨‍💻 Made by **Vikash Goyal**
""")
