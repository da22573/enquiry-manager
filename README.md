# Enquiry Manager

Internal web tool for submitting and reviewing client enquiries. Built for a graduate developer technical challenge.

## What it does

- **Enquiry form** (`/`) — name, email, optional phone (country code + libphonenumber validation), service, description (10–1000 chars)
- **Admin view** (`/admin`) — list enquiries, view details, toggle status (`new` / `reviewed`), search and filter
- Validation on both client and server; SQLite storage; responsive layout

**Stack:** Flask, vanilla JS, SQLite, pytest, Docker

## Run it

### Get the code

**From GitHub:**

```bash
git clone https://github.com/da22573/enquiry-manager.git
cd enquiry-manager
```

**Or from a ZIP:** unzip the folder, then open a terminal inside `enquiry-manager`.

### With Docker (recommended)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/). More detail: [DOCKER-QUICKSTART.md](DOCKER-QUICKSTART.md)

```bash
docker compose up --build
```

Then open http://127.0.0.1:5000/ and http://127.0.0.1:5000/admin in any browser.

Stop with **Ctrl + C**, then `docker compose down`.

### Without Docker

Requires Python 3.9+.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Same URLs as above. Stop with **Ctrl + C**.

## Tests

```bash
pytest
```

Covers validation, enquiry creation, phone rejection, status updates, and admin filtering.

## Assumptions

Where the brief was unclear, I assumed:

| Topic | Assumption |
|-------|------------|
| **Audience** | Internal trusted users — no login on the admin area |
| **Storage** | SQLite file at `data/enquiries.db`, created on first run; not committed to git |
| **Status workflow** | Two states only: `new` and `reviewed` |
| **Services** | Fixed list: Strategy & Planning, Operations, HR & People, Finance |
| **Phone** | Optional; country selector with a short list of regions (UK-focused); stored as E.164 |
| **Deployment** | Local/demo use — Flask dev server, not production-hardened |

## Trade-offs

- Client + server validation duplicated for instant feedback while keeping the API authoritative
- SQLite over JSON for safer writes and SQL filtering; PostgreSQL would be next for production
- Vanilla JS over a framework to stay within the time box; patterns map to a larger stack

## AI usage

Built with assistance from Cursor AI (scaffolding, boilerplate, validation patterns). I reviewed and can explain all of the code.

## Repo

https://github.com/da22573/enquiry-manager
