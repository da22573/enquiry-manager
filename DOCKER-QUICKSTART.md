# Docker quick start

For running this app on any machine. You only need Docker — no Python install.

## 1. Get the code

**From GitHub:**

```bash
git clone https://github.com/da22573/enquiry-manager.git
cd enquiry-manager
```

**Or from a ZIP:** unzip the folder, then open a terminal inside `enquiry-manager`.

## 2. Install Docker

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and make sure it is running.

## 3. Start the app

```bash
docker compose up --build
```

Wait until the terminal shows something like `Running on http://127.0.0.1:5000`.

## 4. Open the app in a browser

Open **any web browser** on the same computer (Chrome, Safari, Firefox, Edge, etc.).

Type or paste one of these addresses into the **address bar**:

| Page | Address |
|------|---------|
| Enquiry form | http://127.0.0.1:5000/ |
| Admin view | http://127.0.0.1:5000/admin |

You do not need to install anything else — Docker keeps the server running in the terminal while you use the browser.

## 5. Stop

Press **Ctrl + C** in the terminal, then:

```bash
docker compose down
```
