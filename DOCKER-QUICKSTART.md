# Enquiry Manager — Docker quick start

Run the app in a container without installing Python locally.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Compose)

## Steps

1. Unzip `enquiry-manager.zip`
2. Open a terminal in the `enquiry-manager` folder
3. Build and start the container:

```bash
cd path/to/enquiry-manager
docker compose up --build
```

4. Open in a browser:

- Enquiry form: http://127.0.0.1:5000/
- Admin view: http://127.0.0.1:5000/admin

The SQLite database is stored in `data/enquiries.db` on your machine via a volume mount, so enquiries persist between container restarts.

## Stop the container

Press **Ctrl + C** in the terminal, then:

```bash
docker compose down
```

## Run in the background (optional)

```bash
docker compose up --build -d
docker compose logs -f    # follow logs; Ctrl + C to stop tailing
docker compose down       # stop and remove the container
```

## Pull from GitHub Container Registry

Images are published to GHCR on every push to `master`:

`ghcr.io/da22573/enquiry-manager:latest`

### Run the published image

```bash
mkdir -p data
docker pull ghcr.io/da22573/enquiry-manager:latest
docker run --rm -p 5000:5000 -v "$(pwd)/data:/app/data" ghcr.io/da22573/enquiry-manager:latest
```

Open http://127.0.0.1:5000/ and http://127.0.0.1:5000/admin as above.

### Make the package public (first time only)

By default, GHCR packages are private. To let others pull without logging in:

1. Open https://github.com/da22573/enquiry-manager/pkgs/container/enquiry-manager
2. **Package settings** → **Change visibility** → **Public**

To pull a private package, log in first:

```bash
echo "$GITHUB_TOKEN" | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
docker pull ghcr.io/da22573/enquiry-manager:latest
```

Use a [Personal Access Token](https://github.com/settings/tokens) with `read:packages` scope.
