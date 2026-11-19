# AI-Powered Customer Review Intelligence System

Independent AI/ML proof of concept for the Cynbit AI/ML Engineer Intern assessment.

## Features
- Sentiment classification using TF-IDF and Logistic Regression
- Test-set evaluation
- Keyword-based complaint category detection
- Template-based suggested responses
- Streamlit interface

## Dataset
Public Hugging Face dataset: `jbeno/sentiment_merged`. This is not Cynbit private data. Review the dataset card and license before redistribution or commercial use.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
- Public dataset may not match real business review language.
- Complaint detection uses keyword rules.
- Replies are templates, not LLM-generated.
- Predictions may be wrong; human review is required.
- No production integration or automatic reply sending.

## Future improvements
- Evaluate on consented, domain-specific business reviews.
- Train a multi-label complaint classifier.
- Add multilingual support.
- Add human approval, monitoring and audit logging.
- Evaluate a guarded LLM response assistant.
