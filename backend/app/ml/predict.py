import os
import threading

import joblib

from app.ml.preprocess import clean_text

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")

_lock = threading.Lock()
_model_cache = None


def _load_model():
    global _model_cache
    with _lock:
        if _model_cache is None:
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(
                    "Model belum dilatih. Jalankan: python -m app.ml.train"
                )
            _model_cache = joblib.load(MODEL_PATH)
        return _model_cache


def reload_model():
    """Force re-reading model.joblib from disk (used after retraining)."""
    global _model_cache
    with _lock:
        _model_cache = None
    return _load_model()


def predict(text: str) -> dict:
    """
    Returns:
        {
          "prediction": "overheating",
          "confidence": 0.91,
          "probabilities": {"overheating": 0.91, "wifi_problem": 0.03, ...},
          "model_version": "v1.0.0",
        }
    """
    bundle = _load_model()
    pipeline = bundle["pipeline"]
    labels = bundle["labels"]

    cleaned = clean_text(text)
    proba = pipeline.predict_proba([cleaned])[0]

    scores = dict(zip(pipeline.classes_, proba))
    # sort descending
    scores = dict(sorted(scores.items(), key=lambda kv: kv[1], reverse=True))
    top_label, top_score = next(iter(scores.items()))

    return {
        "prediction": top_label,
        "confidence": float(top_score),
        "probabilities": {k: float(v) for k, v in scores.items()},
        "model_version": bundle["model_version"],
        "model_name": bundle["model_name"],
    }
