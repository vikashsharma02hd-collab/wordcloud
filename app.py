import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

# Streamlit App
st.set_page_config(page_title="Word Cloud Generator", layout="wide")
st.title("☁️ Word Cloud Generator")

# How it works section
st.markdown("""
### ℹ️ How it works
1. Enter or paste your text into the text area **OR** upload a `.txt` file.
2. The app will process the text and generate a **Word Cloud**.
3. Words appearing more frequently in your text will appear larger in the cloud.
4. You will also see a **bar chart** of the most common words.
5. Useful for exploring themes, keywords, or dominant topics in your data.
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

# Generate word cloud and analysis
if text:
    st.subheader("Generated Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Word frequency analysis
    st.subheader("📊 Word Frequency Analysis")
    words = text.split()
    word_counts = Counter(words)
    common_words = word_counts.most_common(20)

    df = pd.DataFrame(common_words, columns=["Word", "Frequency"])
    st.bar_chart(df.set_index("Word"))

    # Suggestions for more visualizations
    st.subheader("✨ What else can we generate?")
    st.markdown("""
    - **Custom shaped clouds** (circle, heart, star, etc.)
    - **Colored clouds** based on frequency or categories
    - **Stopword filtering** to remove common irrelevant words
    - **Time-based comparison** of text (e.g., trends over time)
    - **Sentiment analysis** alongside the cloud
    """)
else:
    st.info("Please enter text or upload a file to generate a word cloud.")

# Footer
st.markdown("""
---
👨‍💻 Made by **Vikash Goyal**
""")
