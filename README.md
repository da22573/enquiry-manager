# Enquiry Manager

A lightweight internal web tool for submitting and managing client enquiries. Built for a graduate developer technical challenge.

## What it does

- **Public enquiry form** (`/`) — captures name, email, optional phone (with country code), service, and description with client- and server-side validation.
- **Admin view** (`/admin`) — lists enquiries, shows full details in a modal, and lets admins toggle status between `new` and `reviewed`.
- **Search/filter** — filter admin results by name, email, service, or status.
- **Phone validation** — optional phone field with country selector; validated with libphonenumber (stored as E.164, e.g. `+447123456789`).
- **Description limits** — minimum 10 characters, maximum 1000, with a live character counter on the form.
- **Responsive admin** — enquiry list uses a card layout on small screens to avoid horizontal scrolling.

## Tech stack

| Layer | Choice | Why |
|------|--------|-----|
| Frontend | HTML, CSS, vanilla JavaScript | Keeps the UI clear and accessible without framework overhead |
| Backend | Python + Flask | Simple REST API, easy to read and run locally |
| Storage | SQLite (`data/enquiries.db`) | Built into Python; safer than a flat JSON file for reads/writes |
| Phone validation | `phonenumbers` (Python), libphonenumber-js (CDN) | Reliable country-aware phone checks |
| Tests | pytest | Unit and API tests for validation and endpoints |
| Docker | Dockerfile + Compose | One-command setup for reviewers |

## Prerequisites

- **Python 3.9+** — download from [python.org](https://www.python.org/downloads/) if not already installed
- **pip** — included with Python
- **Internet** — required when first loading the enquiry form (phone validation library is loaded from a CDN in the browser). Backend runs offline after `pip install`.

## Set-up

1. Unzip `enquiry-manager.zip`
2. Open a terminal in the `enquiry-manager` folder
3. Run:

```bash
cd path/to/enquiry-manager
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

4. Open in a browser:

- Enquiry form: http://127.0.0.1:5000/
- Admin view: http://127.0.0.1:5000/admin

Stop the server with **Ctrl + C** in the terminal.

**Docker:** see [DOCKER-QUICKSTART.md](DOCKER-QUICKSTART.md) for a one-command container setup (no Python install required).

### Windows notes

- Use `.venv\Scripts\activate` instead of `source .venv/bin/activate`
- If `python3` is not found, try `python` instead

## How to run tests

Tests use **pytest** (installed via `requirements.txt`). You do not need to start the Flask server to run them.

1. Open a terminal in the `enquiry-manager` folder
2. Activate the virtual environment (if not already active):

```bash
cd path/to/enquiry-manager
source .venv/bin/activate          # Windows: .venv\Scripts\activate
```

3. Run all tests:

```bash
pytest
```

You should see output ending with something like `7 passed`.

### Useful test commands

```bash
pytest -v                          # verbose — shows each test name
pytest tests/test_app.py           # run only the main test file
pytest -k filter                   # run tests with "filter" in the name
```

### What the tests cover

- Required field and email validation
- Successful enquiry creation and SQLite persistence
- Invalid phone rejection (optional field)
- Status update (`PATCH`)
- Admin list filtering by service and search query

### If tests fail

| Problem | Fix |
|---------|-----|
| `pytest: command not found` | Run `pip install -r requirements.txt` with venv active |
| `No module named 'phonenumbers'` | Same — reinstall dependencies |
| `No module named 'app'` | Make sure you are in the `enquiry-manager` folder |

## Project structure

```
enquiry-manager/
├── app.py                 # Flask routes and validation
├── db.py                  # SQLite storage and queries
├── phone_utils.py         # Phone validation and country list
├── requirements.txt       # Python dependencies
├── pytest.ini             # Test configuration
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Local Docker setup
├── DOCKER-QUICKSTART.md   # Docker quick start guide
├── data/
│   └── enquiries.db       # Created automatically on first run
├── static/
│   ├── css/styles.css
│   └── js/
│       ├── form.js
│       └── admin.js
├── templates/
│   ├── index.html
│   └── admin.html
└── tests/
    └── test_app.py
```

## Assumptions

- No authentication is required (internal trusted network).
- A SQLite database file is created automatically in `data/` on first run.
- Status values are limited to `new` and `reviewed`.

## Error handling and edge cases

- **Validation** — required fields, email format, description length (10–1000 chars), and phone (libphonenumber) checked on both client and server.
- **HTTP status codes** — `201` created, `400` validation error, `404` enquiry not found.
- **Network errors** — form shows a user-facing message; form data is kept if submission fails.
- **Double submit** — submit button disabled while a request is in progress.
- **Admin** — empty list / no filter matches messaging; status update errors shown to the user.
- **XSS** — user content escaped when rendered in the admin UI (`escapeHtml`).
- **Storage** — SQLite database; created automatically if missing. Uses parameterised queries to avoid SQL injection.

## Accessibility notes

- Semantic labels linked to every input
- Visible focus styles for keyboard users
- Live regions (`aria-live`) for form/admin feedback
- Dialog element for enquiry details
- Responsive layout for mobile and desktop
- **Keyboard navigation:** Form fields, filters, status toggles, and modal close were tested manually with Tab/Enter; visible `:focus-visible` outlines show which control is active
- **`aria-live` feedback:** Success and error messages use `role="status"` and `aria-live="polite"` so screen readers announce submission results and admin actions without a full page reload
- **Known gaps:** Field errors are not yet linked with `aria-describedby` / `aria-invalid`, and no automated WCAG audit (e.g. axe) was run — these would be next steps before production

## Brief notes / trade-offs

With more time I would:

1. **Move to PostgreSQL** for multi-user production hosting and backups.
2. **Add authentication** to the admin area (even basic HTTP auth or SSO).
3. **Use TypeScript on the frontend** for stronger typing as the UI grows.
4. **Expand tests** to cover frontend validation edge cases and optional E2E flows.

Trade-offs made for the time box:

- Chose Flask and vanilla JavaScript over Laravel/Angular to stay focused on clarity within 1–2 hours; the same validation and API patterns would apply in the company's stack.
- Duplicated validation on client and server so users get instant feedback while the API remains the source of truth.
- Used SQLite instead of a flat JSON file for safer storage and SQL-based filtering.

## AI usage disclosure

This project was built with assistance from Cursor AI. I used AI to scaffold the initial project structure, generate boilerplate, and iterate on validation and accessibility patterns. I reviewed, understood, and can explain every part of the code.

## Submission

To create a ZIP for submission (exclude virtual environment and cache files):

```bash
cd ..
zip -r enquiry-manager.zip enquiry-manager -x "*/.venv/*" "*__pycache__*" "*/.pytest_cache/*" "*.DS_Store" "*/data/*.db"
```

Send the ZIP file to the reviewers, or push to a GitHub repo and share the link.
