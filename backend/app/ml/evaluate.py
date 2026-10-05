"""
Print the evaluation metrics produced by the last training run (train.py).

Usage:
    python -m app.ml.evaluate
"""
import json
import os

METRICS_PATH = os.path.join(os.path.dirname(__file__), "metrics.json")


def main():
    if not os.path.exists(METRICS_PATH):
        print("Belum ada metrics.json. Jalankan training dulu: python -m app.ml.train")
        return

    with open(METRICS_PATH) as f:
        metrics = json.load(f)

    print(f"Model version : {metrics['model_version']}")
    print(f"Selected model: {metrics['selected_model']}")
    print(f"Train size    : {metrics['train_size']}  |  Test size: {metrics['test_size']}")

    print("\n5-Fold Cross Validation (F1-macro) — model comparison:")
    for name, res in metrics["model_comparison"].items():
        print(f"  {name:20s} {res['cv_f1_macro_mean']:.4f} (+/- {res['cv_f1_macro_std']:.4f})")

    print("\nTest set classification report:")
    report = metrics["test_classification_report"]
    for label, vals in report.items():
        if isinstance(vals, dict):
            print(
                f"  {label:20s} precision={vals.get('precision', 0):.2f} "
                f"recall={vals.get('recall', 0):.2f} f1={vals.get('f1-score', 0):.2f}"
            )
        else:
            print(f"  {label}: {vals:.4f}")

    print("\nConfusion matrix (rows/cols in label order below):")
    print(metrics["labels"])
    for row in metrics["confusion_matrix"]:
        print(row)


if __name__ == "__main__":
    main()
