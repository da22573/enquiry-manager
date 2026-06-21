# Docker quick start

Run the app on any machine with [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running. No Python required.

Pick **one** option below.

---

## Option A — Pull the published image (no repo needed)

Use this if you only have the GitHub Container Registry image.

**Image:** `ghcr.io/da22573/enquiry-manager:latest`

### 1. Pull and run

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

Wait until the terminal shows `Running on http://127.0.0.1:5000`.

> **Do not run `docker compose up` here** — that command needs the project folder and `docker-compose.yml`. Use `docker run` above instead.

### 2. Open in a browser

On the **same computer**, open any browser and go to:

| Page | Address |
|------|---------|
| Enquiry form | http://127.0.0.1:5000/ |
| Admin view | http://127.0.0.1:5000/admin |

### 3. Stop

Press **Ctrl + C** in the terminal.

### If pull fails (private package)

Log in to GitHub Container Registry first:

```bash
echo YOUR_GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
docker pull ghcr.io/da22573/enquiry-manager:latest
```

Or make the package **public**: GitHub → Packages → enquiry-manager → Package settings → Change visibility.

---

## Option B — Clone the repo and use Compose

Use this if you have the full project folder (clone or ZIP).

### 1. Get the code

```bash
git clone https://github.com/da22573/enquiry-manager.git
cd enquiry-manager
```

Or unzip `enquiry-manager.zip` and open a terminal inside the folder.

### 2. Start the app

```bash
docker compose up --build
```

Wait until the terminal shows `Running on http://127.0.0.1:5000`.

### 3. Open in a browser

| Page | Address |
|------|---------|
| Enquiry form | http://127.0.0.1:5000/ |
| Admin view | http://127.0.0.1:5000/admin |

### 4. Stop

Press **Ctrl + C**, then:

```bash
docker compose down
```
