# Fake News Detection (Beginner-Friendly)

This project detects whether a piece of news text is **REAL** or **FAKE** using:

- NLP text cleaning
- TF-IDF vectorization
- Logistic Regression classification

It also supports basic verification using **Google News RSS** (no scraping) and checks trusted sources:

- The Hindu
- Hindustan Times
- Amar Ujala

> ⚠️ Important: Machine learning predictions and news verification are useful signals, but they are **not guaranteed to be accurate**.

---

## Project Structure

```
fake_news_Detection/
├── app.py                   # Streamlit UI
├── model_training.py        # Model training + evaluation
├── predictor.py             # Prediction helpers
├── preprocessing.py         # Text cleaning + dataset loading
├── news_verification.py     # Google News RSS verification logic
├── requirements.txt         # Python dependencies
├── data/
│   └── news_sample.csv      # Beginner-friendly sample dataset
└── artifacts/               # Saved model after training
```

---

## Setup and Run in VS Code

1. Open this folder in VS Code.
2. Open Terminal in VS Code (`Ctrl + \``).
3. (Recommended) Create and activate a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Train the model:
   ```bash
   python model_training.py
   ```

6. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

7. In the app:
   - Enter news text
   - Click **Predict**
   - Click **Check Google News RSS** to verify against trusted sources

---

## Model Evaluation

When you run `python model_training.py`, it prints:

- Accuracy
- Precision
- Recall
- Confusion Matrix

These metrics help you understand model performance on the sample test split.

---

## Notes for Beginners

- The dataset in `data/news_sample.csv` is small and only for learning/demo purposes.
- For production-quality results, use a larger and better-labeled dataset.
- Verification depends on currently available Google News RSS results and may return no matches.
