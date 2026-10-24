import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

def test_health_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert "VERITRUST" in data["platform"]

def test_demo_login_and_me():
    with TestClient(app) as client:
        res = client.post("/api/auth/demo-login", json={"role": "officer"})
        assert res.status_code == 200
        token = res.json()["access_token"]
        assert token is not None

        # Call /api/auth/me
        res_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert res_me.status_code == 200
        assert res_me.json()["role"] == "officer"

def test_list_applications():
    with TestClient(app) as client:
        login_res = client.post("/api/auth/demo-login", json={"role": "officer"})
        token = login_res.json()["access_token"]
        res = client.get("/api/applications", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        apps = res.json()
        assert len(apps) >= 6

def test_compliance_rules_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/compliance-rules")
        assert res.status_code == 200
        rules = res.json()
        assert len(rules) >= 5

def test_demo_scenarios_list():
    with TestClient(app) as client:
        res = client.get("/api/scenarios")
        assert res.status_code == 200
        scenarios = res.json()
        assert len(scenarios) == 6
