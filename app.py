
import re
import joblib
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Load model files from repository root
model = joblib.load(BASE_DIR / "sentiment_model.joblib")
vectorizer = joblib.load(BASE_DIR / "tfidf_vectorizer.joblib")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-z0-9'\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

ISSUES = {
    "delivery": ["delivery", "late", "delay", "shipping"],
    "product_quality": ["quality", "broken", "damaged", "defective"],
    "customer_support": ["support", "service", "response", "rude"],
    "pricing_payment": ["price", "payment", "refund", "billing"],
    "app_or_website": ["app", "website", "crash", "error"],
    "returns_or_refunds": ["return", "exchange", "refund"]
}

REPLIES = {
    "negative": "We are sorry for your experience. Our team will review your concern and work to improve.",
    "neutral": "Thank you for your feedback. We appreciate your suggestions.",
    "positive": "Thank you for your kind feedback. We appreciate your support."
}

def analyze_review(review):
    cleaned = clean_text(review)
    features = vectorizer.transform([cleaned])

    sentiment = str(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]
    confidence = float(max(probabilities))

    issues = []
    for category, words in ISSUES.items():
        if any(re.search(r"\b" + re.escape(w) + r"\b", cleaned) for w in words):
            issues.append(category)

    if not issues:
        issues = ["general_feedback"]

    reply = REPLIES.get(sentiment, REPLIES["neutral"])

    return sentiment, confidence, issues, reply

st.set_page_config(
    page_title="Customer Review Intelligence",
    page_icon="💬",
    layout="wide"
)

st.title("AI-Powered Customer Review Intelligence")
st.write("Analyze customer reviews using Machine Learning.")

st.info("Independent prototype using a public sentiment dataset. Review suggested replies before use.")

review = st.text_area("Enter a customer review")

if st.button("Analyze Review", disabled=not review.strip()):

    sentiment, confidence, issues, reply = analyze_review(review)

    st.subheader("Analysis Results")

    st.metric("Predicted Sentiment", sentiment.title())
    st.metric("Model Confidence", f"{confidence:.2%}")

    st.write("Detected Issues:")
    st.write(", ".join(issues))

    st.subheader("Suggested Customer Response")
    st.write(reply)

