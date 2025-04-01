import requests

base_url = "http://localhost:8000"


def test_health():
    res = requests.get(f"{base_url}/api/health", timeout=5000)
    assert res.status_code == 200
    assert res.json() == "working"
