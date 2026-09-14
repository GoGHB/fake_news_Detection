"""
Train and evaluate a Fake News Detection model using TF-IDF + Logistic Regression.
"""

import os
from typing import Dict

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from preprocessing import load_dataset


def train_model(data_path: str = "data/news_sample.csv", model_dir: str = "artifacts") -> Dict[str, float]:
    """
    Train model, print beginner-friendly metrics, and save pipeline.
    """
    X, y = load_dataset(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model_pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(stop_words="english", max_df=0.9)),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    model_pipeline.fit(X_train, y_train)

    y_pred = model_pipeline.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, pos_label="REAL", zero_division=0),
        "recall": recall_score(y_test, y_pred, pos_label="REAL", zero_division=0),
    }
    cm = confusion_matrix(y_test, y_pred, labels=["REAL", "FAKE"])

    print("\nModel Evaluation")
    print("-" * 40)
    print(f"Accuracy : {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall   : {metrics['recall']:.4f}")
    print("\nConfusion Matrix (rows=true, cols=pred):")
    print("Labels order: [REAL, FAKE]")
    print(cm)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "fake_news_pipeline.joblib")
    joblib.dump(model_pipeline, model_path)
    print(f"\nSaved trained model to: {model_path}")

    return metrics


if __name__ == "__main__":
    train_model()
