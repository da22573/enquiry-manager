"""Tests for enquiry validation and API behaviour."""

import pytest

from app import create_app, validate_enquiry
from db import fetch_enquiries, init_db
from phone_utils import normalize_phone


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr("db.DATABASE_PATH", db_path)
    init_db()

    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_validate_enquiry_requires_core_fields():
    errors = validate_enquiry({})
    assert "fullName" in errors
    assert "email" in errors
    assert "service" in errors
    assert "description" in errors


def test_validate_enquiry_rejects_invalid_email():
    errors = validate_enquiry(
        {
            "fullName": "Alex Smith",
            "email": "not-an-email",
            "service": "Finance",
            "description": "Need help with quarterly planning.",
        }
    )
    assert errors["email"] == "Enter a valid email address."


def test_create_enquiry_persists_record(client):
    test_client = client
    response = test_client.post(
        "/api/enquiries",
        json={
            "fullName": "Alex Smith",
            "email": "alex@example.com",
            "phoneCountry": "GB",
            "phoneNational": "7123456789",
            "service": "Finance",
            "description": "Need help with quarterly planning.",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["message"] == "Enquiry received"

    stored = fetch_enquiries()
    assert len(stored) == 1
    assert stored[0]["email"] == "alex@example.com"
    assert stored[0]["phone"] == "+447123456789"
    assert stored[0]["status"] == "new"


def test_validate_enquiry_rejects_invalid_phone():
    errors = validate_enquiry(
        {
            "fullName": "Alex Smith",
            "email": "alex@example.com",
            "service": "Finance",
            "description": "Need help with quarterly planning.",
        }
    )
    assert "phone" not in errors

    _e164, phone_error = normalize_phone("GB", "123")
    assert phone_error is not None


def test_create_enquiry_rejects_invalid_phone(client):
    test_client = client
    response = test_client.post(
        "/api/enquiries",
        json={
            "fullName": "Alex Smith",
            "email": "alex@example.com",
            "phoneCountry": "GB",
            "phoneNational": "123",
            "service": "Finance",
            "description": "Need help with quarterly planning.",
        },
    )

    assert response.status_code == 400
    assert "phone" in response.get_json()["errors"]


def test_update_enquiry_status(client):
    test_client = client
    create_response = test_client.post(
        "/api/enquiries",
        json={
            "fullName": "Alex Smith",
            "email": "alex@example.com",
            "service": "Operations",
            "description": "Looking for process improvement support.",
        },
    )
    enquiry_id = create_response.get_json()["enquiry"]["id"]

    patch_response = test_client.patch(
        f"/api/enquiries/{enquiry_id}",
        json={"status": "reviewed"},
    )

    assert patch_response.status_code == 200
    assert patch_response.get_json()["status"] == "reviewed"


def test_list_enquiries_filters_by_status_and_service(client):
    test_client = client

    test_client.post(
        "/api/enquiries",
        json={
            "fullName": "Alex Smith",
            "email": "alex@example.com",
            "service": "Finance",
            "description": "Need help with quarterly planning.",
        },
    )
    test_client.post(
        "/api/enquiries",
        json={
            "fullName": "Jordan Lee",
            "email": "jordan@example.com",
            "service": "Operations",
            "description": "Looking for process improvement support.",
        },
    )

    finance_response = test_client.get("/api/enquiries?service=Finance")
    assert finance_response.status_code == 200
    finance_results = finance_response.get_json()
    assert len(finance_results) == 1
    assert finance_results[0]["fullName"] == "Alex Smith"

    search_response = test_client.get("/api/enquiries?q=jordan")
    assert search_response.status_code == 200
    search_results = search_response.get_json()
    assert len(search_results) == 1
    assert search_results[0]["email"] == "jordan@example.com"
