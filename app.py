"""
Streamlit app for Fake News Detection.
"""

import streamlit as st

from news_verification import verify_with_trusted_sources
from predictor import predict_news

st.set_page_config(page_title="Fake News Detection", page_icon="📰")
st.title("📰 Fake News Detection App")
st.write(
    "Enter a news statement below. The app predicts whether it looks REAL or FAKE "
    "using a machine learning model."
)

news_input = st.text_area("News text", height=180, placeholder="Paste a headline or short article...")

if st.button("Predict"):
    if not news_input.strip():
        st.warning("Please enter some news text.")
    else:
        try:
            result = predict_news(news_input)
            st.subheader(f"Prediction: **{result['label']}**")
            if result["confidence"] is not None:
                st.write(f"Model confidence: **{result['confidence'] * 100:.2f}%**")
        except FileNotFoundError as error:
            st.error(str(error))

st.divider()
st.subheader("Verify with trusted sources")

if st.button("Check Google News RSS"):
    if not news_input.strip():
        st.warning("Please enter some news text first.")
    else:
        with st.spinner("Checking Google News RSS..."):
            verification = verify_with_trusted_sources(news_input)

        for source, articles in verification.items():
            st.markdown(f"### {source}")
            if not articles:
                st.write("No relevant article found right now.")
                continue
            for article in articles:
                st.markdown(f"- [{article['title']}]({article['link']})")
                if article["published"]:
                    st.caption(f"Published: {article['published']}")

st.info(
    "Important: Machine learning predictions and online news verification are helpful indicators "
    "but are **not guaranteed to be accurate**."
)
