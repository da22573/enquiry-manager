"""Enquiry management API and page routes."""

from __future__ import annotations

import os
import re
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

from db import fetch_enquiries, init_db, insert_enquiry, update_enquiry_status
from phone_utils import PHONE_COUNTRIES, normalize_phone

SERVICES = [
    "Strategy & Planning",
    "Operations",
    "HR & People",
    "Finance",
]

STATUSES = ["new", "reviewed"]

EMAIL_MAX_LENGTH = 254
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def create_app() -> Flask:
    app = Flask(__name__)
    init_db()

    @app.route("/")
    def enquiry_form():
        return render_template(
            "index.html",
            services=SERVICES,
            phone_countries=PHONE_COUNTRIES,
        )

    @app.route("/admin")
    def admin_view():
        return render_template("admin.html", services=SERVICES, statuses=STATUSES)

    @app.post("/api/enquiries")
    def create_enquiry():
        payload = request.get_json(silent=True) or {}
        errors = validate_enquiry(payload)
        if errors:
            return jsonify({"errors": errors}), 400

        phone, phone_error = normalize_phone(
            payload.get("phoneCountry", ""),
            payload.get("phoneNational", ""),
        )
        if phone_error:
            return jsonify({"errors": {"phone": phone_error}}), 400

        enquiry = {
            "id": str(uuid.uuid4()),
            "fullName": payload["fullName"].strip(),
            "email": payload["email"].strip().lower(),
            "phone": phone,
            "service": payload["service"],
            "description": payload["description"].strip(),
            "status": "new",
            "submittedAt": datetime.now(timezone.utc).isoformat(),
        }

        insert_enquiry(enquiry)

        return jsonify({"message": "Enquiry received", "enquiry": enquiry}), 201

    @app.get("/api/enquiries")
    def list_enquiries():
        query = request.args.get("q", "").strip().lower()
        service = request.args.get("service", "").strip()
        status = request.args.get("status", "").strip()

        return jsonify(fetch_enquiries(query=query, service=service, status=status))

    @app.patch("/api/enquiries/<enquiry_id>")
    def update_enquiry(enquiry_id: str):
        payload = request.get_json(silent=True) or {}
        status = payload.get("status")

        if status not in STATUSES:
            return jsonify({"errors": {"status": "Status must be 'new' or 'reviewed'"}}), 400

        enquiry = update_enquiry_status(enquiry_id, status)
        if enquiry is None:
            return jsonify({"errors": {"id": "Enquiry not found"}}), 404

        return jsonify(enquiry)

    return app


def validate_enquiry(payload: dict) -> dict[str, str]:
    errors: dict[str, str] = {}

    full_name = (payload.get("fullName") or "").strip()
    email = (payload.get("email") or "").strip()
    service = (payload.get("service") or "").strip()
    description = (payload.get("description") or "").strip()

    if not full_name:
        errors["fullName"] = "Full name is required."
    elif len(full_name) > 100:
        errors["fullName"] = "Full name must be 100 characters or fewer."

    if not email:
        errors["email"] = "Email address is required."
    elif len(email) > EMAIL_MAX_LENGTH or not EMAIL_PATTERN.match(email):
        errors["email"] = "Enter a valid email address."

    if not service:
        errors["service"] = "Please select a service."
    elif service not in SERVICES:
        errors["service"] = "Please choose a valid service."

    if not description:
        errors["description"] = "Please describe your enquiry."
    elif len(description) < 10:
        errors["description"] = "Description must be at least 10 characters."
    elif len(description) > 1000:
        errors["description"] = "Description must be 1000 characters or fewer."

    return errors


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=port)
