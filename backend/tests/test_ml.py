from app.ml.predict import predict


def test_predict_overheating():
    result = predict("Laptop saya sangat panas dan mati sendiri setelah dipakai lama")
    assert result["prediction"] == "overheating"
    assert 0.0 <= result["confidence"] <= 1.0


def test_predict_wifi_problem():
    result = predict("Wifi laptop tidak bisa konek ke jaringan sama sekali")
    assert result["prediction"] == "wifi_problem"


def test_predict_returns_all_class_probabilities():
    result = predict("Laptop saya lemot sekali")
    assert len(result["probabilities"]) == 10
    assert abs(sum(result["probabilities"].values()) - 1.0) < 0.01


def test_predict_model_version_present():
    result = predict("keyboard tidak berfungsi")
    assert result["model_version"]
