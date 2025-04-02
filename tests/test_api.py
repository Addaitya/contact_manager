from typing import Optional

import requests
from pydantic import BaseModel

base_url = "http://localhost:8000/api"


def test_health():
    """Check health"""
    res = requests.get(f"{base_url}/health", timeout=5000)
    assert res.status_code == 200
    assert res.json() == "working"


def test_get_contacts():
    """Test get pagenated contacts api."""
    res = requests.get(f"{base_url}/contacts", params={"page": 0, "limit": 10})
    assert res.status_code == 200
    data = res.json()
    fields = ["contacts", "prev", "next", "limit", "page", "total"]

    for field in fields:
        assert field in data, f"Field '{field}' not found"


def test_add_contact():
    """Test add contact api."""
    contact_info = {
        "name": "Naman",
        "email": "Naman@gmail.com",
        "code": "+91",
        "number": "9458433243",
    }

    res = requests.post(f"{base_url}/contacts", json=contact_info)

    assert res.status_code == 200


def test_email_validation():
    """Test email validation of add contact api."""
    contact_info = {
        "name": "Naman",
        "email": "Naman-row@gmailcom",
        "code": "+91",
        "number": "9458433243",
    }

    res = requests.post(f"{base_url}/contacts", json=contact_info)

    assert res.status_code == 422


def test_number_validation():
    """Test number validation of add contact api."""
    contact_info = {
        "name": "Naman",
        "email": "Naman-row@gmail.com",
        "code": "+91",
        "number": "012345678910",
    }

    res = requests.post(f"{base_url}/contacts", json=contact_info)

    assert res.status_code == 422
