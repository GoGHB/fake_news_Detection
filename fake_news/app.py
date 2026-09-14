"""
Fake News Detector - Hybrid App (ML Model + Google News Verification)
-------------------------------------------------------------------------
Isi folder mein yeh files honi chahiye:
    - app.py                 (yeh file)
    - fake_news_model.pkl
    - tfidf_vectorizer.pkl
    - news_verifier.py       (Google News check wala module)

Setup:
    python -m pip install streamlit scikit-learn joblib pygooglenews feedparser --break-system-packages

Run:
    python -m streamlit run app.py
"""

import re
import streamlit as st
import joblib
from news_verifier import verify_claim

# ---------------- Page Config ----------------
st.set_page_config(page_title="Fake News Detector", page_icon="📰", layout="wide")

# ---------------- Sidebar: Declaration Box ----------------
with st.sidebar:
    st.header("📋 Declaration")

    st.subheader("Dataset Coverage")
    st.write("ML model niche diye gaye years ki news pe train hua hai:")
    st.table({
        "Year": ["2015", "2016", "2017", "2018"],
        "Articles": ["1,598", "13,915", "23,104", "35"]
    })
    st.caption(
        "Bulk data 2016-2017 (US politics) ka hai. Isliye ML model purane "
        "writing patterns pe based hai — aaj ki fresh news ke liye utna "
        "reliable nahi hai."
    )

    st.subheader("Google News Checker")
    st.write(
        "Isi wajah se yeh app mein ek **real-time Google News check** bhi "
        "add kiya gaya hai — jo current/live news ko trusted sources "
        "(Reuters, BBC, etc.) se cross-verify karta hai, taaki sirf "
        "purane pattern pe depend na rehna pade."
    )

# ---------------- Load ML Model (cached) ----------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("fake_news_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_artifacts()


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def ml_predict(text):
    cleaned = clean_text(text)
    features = vectorizer.transform([cleaned])
    pred = model.predict(features)[0]
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = model.predict_proba(features)[0][pred]
    label = "Real" if pred == 1 else "Fake"
    return label, confidence


# ---------------- UI ----------------
st.title("📰 Fake News Detector")
st.write(
    "Yeh app do tarah se check karta hai: pehle **Google News** pe recent trusted "
    "coverage dhoondta hai, uske baad **ML model** (language pattern) se prediction deta hai."
)

user_input = st.text_area(
    "News Headline / Article Text",
    height=180,
    placeholder="Yahan news ka text paste karo..."
)

use_live_check = st.checkbox("Google News se real-time verify bhi karo", value=True)

if st.button("Check News", type="primary"):
    if not user_input.strip():
        st.warning("Pehle kuch text daalo.")
    else:
        # ---------- Step 1: Google News real-time check ----------
        news_result = None
        if use_live_check:
            with st.spinner("Google News check kar rahe hain..."):
                try:
                    news_result = verify_claim(user_input)
                except Exception as e:
                    st.info(f"Google News check fail ho gaya (internet/library issue): {e}")

        if news_result:
            st.subheader("🌐 Real-Time News Check")
            st.write(f"**Verdict:** {news_result['verdict']}")
            st.write(f"Trusted source matches: {news_result['trusted_source_matches']} "
                      f"/ {news_result['total_articles_found']} total articles found")

            if news_result["trusted_articles"]:
                with st.expander("Matching trusted articles dekho"):
                    for art in news_result["trusted_articles"][:5]:
                        st.markdown(f"- [{art['title']}]({art['link']}) — *{art['source']}*")

        # ---------- Step 2: ML model prediction (hamesha dikhao, fallback ke roop mein) ----------
        label, confidence = ml_predict(user_input)

        st.subheader("🤖 ML Model Prediction (language pattern based)")
        if label == "Real":
            st.success(f"Prediction: **{label}**")
        else:
            st.error(f"Prediction: **{label}**")

        if confidence is not None:
            st.metric("Confidence", f"{confidence*100:.1f}%")
            st.progress(float(confidence))

        st.caption(
            "⚠️ Google News check sirf tab kaam karta hai jab internet available ho. "
            "Dono signals ko saath mein dekho — sirf ek pe bharosa mat karo. Yeh tool "
            "fact-checking ka replacement nahi hai."
        )

st.divider()
st.caption("Built with scikit-learn (TF-IDF + Logistic Regression) + Google News RSS · Trained on cleaned Kaggle Fake/Real News dataset")