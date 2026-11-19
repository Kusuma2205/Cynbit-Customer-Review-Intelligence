
import re
import joblib
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
model = joblib.load(MODEL_DIR / "sentiment_model.joblib")
vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.joblib")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-z0-9'\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

ISSUES = {
    "delivery": ["delivery", "delivered", "shipping", "shipment", "late", "delay", "arrived"],
    "product_quality": ["quality", "broken", "damaged", "defective", "faulty", "poor"],
    "customer_support": ["support", "service", "staff", "response", "respond", "rude"],
    "pricing_payment": ["price", "cost", "expensive", "charge", "payment", "billing"],
    "app_or_website": ["app", "website", "login", "crash", "error", "slow", "loading"],
    "returns_or_refunds": ["return", "exchange", "refund", "replacement"]
}
REPLIES = {
    "negative": "We are sorry for your experience. Thank you for bringing this to our attention. Our team will review the issue and work to improve.",
    "neutral": "Thank you for sharing your feedback. We appreciate your suggestions and will use them to improve our service.",
    "positive": "Thank you for your kind feedback! We are happy to hear about your experience and appreciate your support."
}

def analyze(review):
    cleaned = clean_text(review)
    x = vectorizer.transform([cleaned])
    sentiment = str(model.predict(x)[0])
    probs = model.predict_proba(x)[0]
    found = []
    for category, words in ISSUES.items():
        if any(re.search(r"\b" + re.escape(word) + r"\b", cleaned) for word in words):
            found.append(category)
    if not found:
        found = ["general_feedback"]
    return sentiment, float(max(probs)), found, REPLIES.get(sentiment, REPLIES["neutral"])

st.set_page_config(page_title="Customer Review Intelligence", page_icon="💬", layout="wide")
st.title("AI-Powered Customer Review Intelligence")
st.caption("Cynbit AI/ML Engineer Intern assessment – independent proof of concept")
st.info("Public-dataset prototype. Suggested replies are drafts; review before sending.")
review = st.text_area("Enter a customer review", height=130)
if st.button("Analyze review", type="primary", disabled=not review.strip()):
    sentiment, confidence, issues, reply = analyze(review)
    c1, c2 = st.columns(2)
    c1.metric("Predicted sentiment", sentiment.title())
    c2.metric("Model confidence", f"{confidence:.1%}")
    st.subheader("Detected issue categories")
    st.write(", ".join(issues))
    st.subheader("Suggested response (review before sending)")
    st.write(reply)
st.caption("Not connected to customer accounts, review platforms or Cynbit production systems.")
