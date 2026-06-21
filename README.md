# Enquiry Manager

Internal web tool for submitting and reviewing client enquiries. Built for a graduate developer technical challenge.

## What it does

- **Enquiry form** (`/`) — name, email, optional phone (country code + libphonenumber validation), service, description (10–1000 chars)
- **Admin view** (`/admin`) — list enquiries, view details, toggle status (`new` / `reviewed`), search and filter
- Validation on both client and server; SQLite storage; responsive layout

**Stack:** Flask, vanilla JS, SQLite, pytest, Docker

## Run it

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Docker path) or **Python 3.9+** (without Docker).

Full Docker steps: [DOCKER-QUICKSTART.md](DOCKER-QUICKSTART.md)

### Option 1 — Docker image from GitHub Container Registry

No repo clone needed. Pull the published image and run it:

**Mac / Linux:**

```bash
mkdir -p data
docker pull ghcr.io/da22573/enquiry-manager:latest
docker run --rm -p 5000:5000 -v "$(pwd)/data:/app/data" ghcr.io/da22573/enquiry-manager:latest
```

**Windows (PowerShell):**

```powershell
mkdir data
docker pull ghcr.io/da22573/enquiry-manager:latest
docker run --rm -p 5000:5000 -v "${PWD}/data:/app/data" ghcr.io/da22573/enquiry-manager:latest
```

Use **`docker run`**, not `docker compose up` — Compose needs the project files.

### Option 2 — Docker from source (clone + Compose)

**Get the code:**

```bash
git clone https://github.com/da22573/enquiry-manager.git
cd enquiry-manager
```

Or unzip the project folder and open a terminal inside it.

**Start the app:**

```bash
docker compose up --build
```

Stop with **Ctrl + C**, then `docker compose down`.

### Option 3 — Without Docker

**Get the code** (clone or unzip as above), then:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Stop with **Ctrl + C**.

### Open the app

Once the server is running, open **any browser on the same machine**:

- Enquiry form: http://127.0.0.1:5000/
- Admin view: http://127.0.0.1:5000/admin

Leave the terminal open while you use the app.

## Tests

From the project folder, with dependencies installed:

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

**Published image:** `ghcr.io/da22573/enquiry-manager:latest`
