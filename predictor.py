"""
Prediction helpers for the Fake News Detection model.
"""

import os
from typing import Dict

import joblib

from preprocessing import clean_text

DEFAULT_MODEL_PATH = "artifacts/fake_news_pipeline.joblib"


def load_model(model_path: str = DEFAULT_MODEL_PATH):
    """
    Load a previously trained pipeline from disk.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at '{model_path}'. Run `python model_training.py` first."
        )
    return joblib.load(model_path)


def predict_news(news_text: str, model_path: str = DEFAULT_MODEL_PATH) -> Dict[str, float]:
    """
    Predict whether a news statement is REAL or FAKE.
    """
    model = load_model(model_path)
    prepared_text = clean_text(news_text)
    prediction = model.predict([prepared_text])[0]

    confidence = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([prepared_text])[0]
        classes = list(model.classes_)
        confidence = float(probabilities[classes.index(prediction)])

    return {"label": prediction, "confidence": confidence}
