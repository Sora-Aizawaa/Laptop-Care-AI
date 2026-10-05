"""
Train the LaptopCare AI text classification model.

Pipeline:
  Raw complaint -> clean_text -> TF-IDF -> classifier -> probability -> prediction

Usage:
    python -m app.ml.train
"""
import json
import os

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

from app.ml.preprocess import clean_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "laptop_complaints.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")
METRICS_PATH = os.path.join(os.path.dirname(__file__), "metrics.json")
MODEL_VERSION = "v1.0.0"


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH)
    df = df.dropna(subset=["text", "label"])
    df["text"] = df["text"].apply(clean_text)
    return df


def build_candidates():
    return {
        "logistic_regression": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=1000)),
        ]),
        "linear_svm": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            # CalibratedClassifierCV wraps LinearSVC so predict_proba is
            # available for confidence scoring, same as the other models.
            ("clf", CalibratedClassifierCV(LinearSVC(), cv=3)),
        ]),
        "naive_bayes": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", MultinomialNB()),
        ]),
    }


def main():
    df = load_dataset()
    X, y = df["text"], df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    candidates = build_candidates()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    comparison = {}
    for name, pipeline in candidates.items():
        scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1_macro")
        comparison[name] = {
            "cv_f1_macro_mean": round(scores.mean(), 4),
            "cv_f1_macro_std": round(scores.std(), 4),
        }
        print(f"{name}: CV F1-macro = {scores.mean():.4f} (+/- {scores.std():.4f})")

    # Select best candidate by CV F1-macro (baseline recommendation: logistic regression)
    best_name = max(comparison, key=lambda n: comparison[n]["cv_f1_macro_mean"])
    best_pipeline = candidates[best_name]
    print(f"\nSelected model: {best_name}")

    best_pipeline.fit(X_train, y_train)
    y_pred = best_pipeline.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, y_pred).tolist()
    labels = sorted(y.unique().tolist())

    print("\nClassification report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    joblib.dump(
        {
            "pipeline": best_pipeline,
            "labels": labels,
            "model_name": best_name,
            "model_version": MODEL_VERSION,
            "supports_proba": hasattr(best_pipeline.named_steps["clf"], "predict_proba"),
        },
        MODEL_PATH,
    )

    metrics = {
        "model_version": MODEL_VERSION,
        "selected_model": best_name,
        "model_comparison": comparison,
        "test_classification_report": report,
        "confusion_matrix": cm,
        "labels": labels,
        "train_size": len(X_train),
        "test_size": len(X_test),
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nModel saved to {MODEL_PATH}")
    print(f"Metrics saved to {METRICS_PATH}")


if __name__ == "__main__":
    main()
