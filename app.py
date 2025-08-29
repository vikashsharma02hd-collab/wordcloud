import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
from PIL import Image
import io

# Download required NLTK data automatically
nltk.download("stopwords")
nltk.download("vader_lexicon")

# Streamlit App
st.set_page_config(page_title="Word Cloud Generator", layout="wide")
st.title("☁️ Word Cloud Generator")

# How it works section
st.markdown("""
### ℹ️ How it works
1. Enter or paste your text into the text area **OR** upload a `.txt` file.
2. Choose options like **shape, colors, and stopword filtering**.
3. The app generates a **Word Cloud** and shows a **bar chart** of frequent words.
4. Upload multiple files for **time-based comparison**.
5. Get a quick **sentiment analysis** of your text.
""")

# Text input
st.subheader("Enter text")
text_input = st.text_area("Paste your text here", height=200)

# File uploader (multiple for comparison)
st.subheader("Or upload one or more text files")
uploaded_files = st.file_uploader("Upload .txt files", type=["txt"], accept_multiple_files=True)

text = ""
if uploaded_files:
    texts = [f.read().decode("utf-8") for f in uploaded_files]
    text = " ".join(texts)
elif text_input.strip() != "":
    text = text_input

# Options
st.sidebar.header("⚙️ Options")
shape_option = st.sidebar.selectbox("Choose Word Cloud Shape", ["Default", "Circle", "Heart", "Star"])
color_option = st.sidebar.selectbox("Color Style", ["Frequency-based", "Random"])
remove_stopwords = st.sidebar.checkbox("Remove Stopwords", value=True)

# Stopwords
stop_words = set(stopwords.words("english")) if remove_stopwords else None

# Shape masks
mask = None
if shape_option != "Default":
    if shape_option == "Circle":
        x, y = np.ogrid[:300, :300]
        mask = (x - 150) ** 2 + (y - 150) ** 2 > 140 ** 2
        mask = 255 * mask.astype(int)
    elif shape_option == "Heart":
        x = np.linspace(-1.5, 1.5, 300)
        y = np.linspace(-1.5, 1.5, 300)
        x, y = np.meshgrid(x, y)
        mask = (x**2 + y**2 - 1)**3 - x**2 * y**3 <= 0
        mask = 255 * mask.astype(int)
    elif shape_option == "Star":
        mask = np.full((300, 300), 255, dtype=int)
        for i in range(5):
            for r in range(80, 140):
                angle = i * (2 * np.pi / 5) + np.linspace(0, 2*np.pi/5, 60)
                x = (150 + r * np.cos(angle)).astype(int)
                y = (150 + r * np.sin(angle)).astype(int)
                mask[y, x] = 0

# Generate word cloud and analysis
if text:
    st.subheader("Generated Word Cloud")
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=stop_words,
        mask=mask,
        colormap="viridis" if color_option == "Frequency-based" else None
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Word frequency analysis
    st.subheader("📊 Word Frequency Analysis")
    words = [w for w in text.split() if not remove_stopwords or w.lower() not in stop_words]
    word_counts = Counter(words)
    common_words = word_counts.most_common(20)

    df = pd.DataFrame(common_words, columns=["Word", "Frequency"])
    st.bar_chart(df.set_index("Word"))

    # Time-based comparison
    if uploaded_files and len(uploaded_files) > 1:
        st.subheader("⏳ Time-based Comparison")
        comparison_data = {f.name: Counter(t.split()).most_common(5) for f, t in zip(uploaded_files, texts)}
        comp_df = pd.DataFrame({k: dict(v) for k, v in comparison_data.items()}).fillna(0)
        st.dataframe(comp_df)

    # Sentiment analysis
    st.subheader("💬 Sentiment Analysis")
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    st.json(sentiment)
else:
    st.info("Please enter text or upload a file to generate a word cloud.")

# Footer
st.markdown("""
---
👨‍💻 Made by **Vikash Goyal**
""")
