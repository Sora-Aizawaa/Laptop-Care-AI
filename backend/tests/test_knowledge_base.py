def test_list_categories(client):
    resp = client.get("/api/categories")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 6
    names = {c["name"] for c in data}
    assert "Hardware" in names


def test_list_problems(client):
    resp = client.get("/api/problems")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 10


def test_get_problem_detail(client):
    problems = client.get("/api/problems").json()
    problem_id = problems[0]["id"]
    resp = client.get(f"/api/problems/{problem_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert "troubleshooting_steps" in data
    assert len(data["troubleshooting_steps"]) > 0


def test_get_problem_not_found(client):
    resp = client.get("/api/problems/999999")
    assert resp.status_code == 404


def test_history_endpoint(client):
    client.post("/api/diagnosis", json={"complaint": "Laptop saya sangat lambat sekali ketika membuka aplikasi"})
    resp = client.get("/api/history")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_dashboard_statistics(client):
    resp = client.get("/api/dashboard/statistics")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_diagnoses" in data
    assert "most_common_problems" in data


def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
