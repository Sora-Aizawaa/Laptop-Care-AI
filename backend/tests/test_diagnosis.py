def test_diagnosis_high_confidence_overheating(client):
    resp = client.post(
        "/api/diagnosis",
        json={"complaint": "Laptop saya sangat panas dan tiba tiba mati setelah dipakai 30 menit, kipas sangat berisik"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["diagnosis"]["problem"] == "Overheating"
    assert data["priority"] in ("HIGH", "CRITICAL")
    assert len(data["troubleshooting_steps"]) > 0


def test_diagnosis_invalid_input_returns_400(client):
    resp = client.post("/api/diagnosis", json={"complaint": ""})
    assert resp.status_code == 400
    assert "message" in resp.json()


def test_diagnosis_ambiguous_complaint_asks_follow_up(client):
    resp = client.post("/api/diagnosis", json={"complaint": "laptop saya bermasalah"})
    assert resp.status_code == 200
    data = resp.json()
    # Ambiguous input should either be low-confidence (follow-up questions)
    # or resolve to a specific, valid category — never crash.
    if data["diagnosis"]["is_low_confidence"]:
        assert len(data["follow_up_questions"]) > 0
    else:
        assert data["diagnosis"]["problem"] is not None


def test_get_diagnosis_by_id(client):
    create_resp = client.post(
        "/api/diagnosis",
        json={"complaint": "Wifi laptop saya tidak muncul sama sekali di daftar jaringan"},
    )
    diagnosis_id = create_resp.json()["diagnosis_id"]
    if diagnosis_id is not None:
        resp = client.get(f"/api/diagnosis/{diagnosis_id}")
        assert resp.status_code == 200
        assert resp.json()["diagnosis_id"] == diagnosis_id


def test_get_diagnosis_not_found(client):
    resp = client.get("/api/diagnosis/999999")
    assert resp.status_code == 404


def test_submit_feedback(client):
    create_resp = client.post(
        "/api/diagnosis",
        json={"complaint": "Keyboard laptop saya beberapa tombol tidak berfungsi sama sekali"},
    )
    diagnosis_id = create_resp.json()["diagnosis_id"]
    if diagnosis_id is not None:
        resp = client.post(f"/api/diagnosis/{diagnosis_id}/feedback", json={"is_correct": True})
        assert resp.status_code == 200
