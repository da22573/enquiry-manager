"""Phone number parsing and validation using Google's libphonenumber."""

from __future__ import annotations

import phonenumbers
from phonenumbers import NumberParseException

# ISO region code, international dial code, display name.
# Kept as a short list suitable for a UK-based firm; easy to extend.
PHONE_COUNTRIES = [
    {"region": "GB", "dial_code": "+44", "name": "United Kingdom"},
    {"region": "IE", "dial_code": "+353", "name": "Ireland"},
    {"region": "US", "dial_code": "+1", "name": "United States"},
    {"region": "CA", "dial_code": "+1", "name": "Canada"},
    {"region": "FR", "dial_code": "+33", "name": "France"},
    {"region": "DE", "dial_code": "+49", "name": "Germany"},
    {"region": "ES", "dial_code": "+34", "name": "Spain"},
    {"region": "IT", "dial_code": "+39", "name": "Italy"},
    {"region": "NL", "dial_code": "+31", "name": "Netherlands"},
    {"region": "AU", "dial_code": "+61", "name": "Australia"},
    {"region": "IN", "dial_code": "+91", "name": "India"},
]

ALLOWED_REGIONS = {country["region"] for country in PHONE_COUNTRIES}


def normalize_phone(region: str, national_number: str) -> tuple[str, str | None]:
    """
    Validate and format a phone number.

    Returns:
        (e164_string, None) on success — e.g. ("+447123456789", None)
        ("", error_message) on failure
        ("", None) when phone is optional and left blank
    """
    national_number = (national_number or "").strip()

    if not national_number:
        return "", None

    region = (region or "").strip().upper()
    if region not in ALLOWED_REGIONS:
        return "", "Please select a valid country code."

    try:
        parsed = phonenumbers.parse(national_number, region)
    except NumberParseException:
        return "", "Enter a valid phone number for the selected country."

    if not phonenumbers.is_valid_number(parsed):
        return "", "Enter a valid phone number for the selected country."

    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    return e164, None
