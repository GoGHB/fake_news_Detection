"""
Text preprocessing helpers for the Fake News Detection project.
"""

import re
from typing import Tuple

import pandas as pd


def clean_text(text: str) -> str:
    """
    Clean raw news text with simple beginner-friendly NLP steps.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\\S+|www\\.\\S+", " ", text)  # remove links
    text = re.sub(r"[^a-zA-Z\\s]", " ", text)  # keep only letters and spaces
    text = re.sub(r"\\s+", " ", text).strip()  # normalize extra spaces
    return text


def load_dataset(csv_path: str) -> Tuple[pd.Series, pd.Series]:
    """
    Load a CSV file with `text` and `label` columns and return cleaned text + labels.
    """
    df = pd.read_csv(csv_path)
    required_columns = {"text", "label"}
    if not required_columns.issubset(df.columns):
        raise ValueError("Dataset must contain 'text' and 'label' columns.")

    df = df.dropna(subset=["text", "label"]).copy()
    df["text"] = df["text"].apply(clean_text)
    df["label"] = df["label"].str.upper().str.strip()
    df = df[df["label"].isin(["REAL", "FAKE"])]

    if df.empty:
        raise ValueError("No valid rows found. Labels must be REAL or FAKE.")

    return df["text"], df["label"]
