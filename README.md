# Diagnostic Test Dashboard

A multi-page Streamlit app for exploring and analyzing an Essential Diagnostics List (EDL) for Universal Health Coverage research. All data is loaded from a single CSV file — no backend database.

---

## Running Locally

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Home.py
```

The app runs at `http://localhost:8501` by default.

---

## App Overview

### Pages

| Page | Purpose |
|---|---|
| `Home.py` | Landing page, initializes session state |
| `pages/1_Diagnostic_Test_Dashboard.py` | Main explorer with sidebar filters and tabbed views |
| `pages/2_Build_Custom_Condition_Tier.py` | Build or upload a custom condition-level filter |
| `pages/3_Build_Custom_Test_Tier.py` | Build or upload a custom test-format filter |
| `pages/4_Diagnostic_Test_Summary.py` | Generate and export a diagnostic placement summary |

### Key Files

```
static/
  tableau3_t2_tjfs_join_edl_dashadmin.csv   ← master dataset (single source of truth)
  lancet_condition_level.csv                ← Lancet reference condition tiers
  lancet_test_tier.csv                      ← Lancet reference test-format tiers

.streamlit/
  config.toml                               ← Streamlit server + browser config

utils/
  dataframe_utils/filter.py                 ← sidebar filter label → column mapping
  dataframe_utils/utils.py                  ← filter/query/grid helpers
  dataframe_utils/utils_center_tab.py       ← per-tab DataFrame functions
  condition_tier_utils/utils.py             ← page 2 logic
  test_tier_utils/utils.py                  ← page 3 logic
  tests_summary_utils/utils.py              ← page 4 logic + PDF export
```

---

## Production Deployment

The app runs on a single Ubuntu server behind an nginx reverse proxy, containerized with Docker Compose.

### Server Details

| Item | Value |
|---|---|
| Server | `lee-edl.miserver.it.umich.edu` |
| IP | `141.211.145.96` |
| User | `yechank` |
| Deployment directory | `~/diagnostic_project/` |
| nginx config directory | `~/nginx/conf.d/` |

### Network Flow

```
User browser
  → http://141.211.145.96 (port 80)
    → nginx container (port 80)
      → streamlit_app container (port 8501)
        → Streamlit processes request and responds
      ← response back through nginx
  ← back to browser
```

nginx also handles WebSocket upgrades, which Streamlit requires for its live browser connection.

### First-Time Server Setup

These steps only need to be done once on a fresh server.

**1. Install Docker Engine**

Follow the official guide: https://docs.docker.com/engine/install/ubuntu/

**2. Create the deployment directory**

```bash
mkdir -p ~/diagnostic_project
```

**3. Create the nginx config directory and configuration file**

```bash
mkdir -p ~/nginx/conf.d
nano ~/nginx/conf.d/streamlit.conf
```

Paste the following into `streamlit.conf`:

```nginx
upstream streamlit_app {
    server streamlit_app:8501;
}

server {
    listen 80;

    location / {
        proxy_pass http://streamlit_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_buffering off;
        proxy_read_timeout 86400;
    }
}
```

**4. Create the Dockerfile on the server**

```bash
nano ~/diagnostic_project/Dockerfile
```

Paste the following:

```dockerfile
FROM python:3.10.0

WORKDIR /app/
RUN git clone https://github.com/yckumich/diagnostic.git
WORKDIR /app/diagnostic
RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "Home.py"]
```

---

### Deployment Cheat Sheet (Repeatable Updates)

Use this every time you push a new version of the app.

**Step 1 — Commit and push changes to GitHub (local machine)**

```bash
git add .
git commit -m "Describe what you updated"
git push origin main
```

**Step 2 — Copy updated docker-compose.yml to server (local machine)**

```bash
scp docker-compose.yml yechank@lee-edl.miserver.it.umich.edu:/home/yechank/diagnostic_project/
```

**Step 3 — SSH into the server**

```bash
ssh yechank@lee-edl.miserver.it.umich.edu
cd ~/diagnostic_project
```

**Step 4 — Build a new Docker image**

```bash
sudo docker build --no-cache -t diagnostic:0.0.X .
```

Replace `0.0.X` with the next version number (e.g. `0.0.7`). Always bump the tag — it avoids any risk of running a cached old image.

**Step 5 — Update the image tag in docker-compose.yml**

```bash
nano docker-compose.yml
```

Update this line to match the new tag:

```yaml
image: diagnostic:0.0.X
```

**Step 6 — Restart the stack**

```bash
sudo docker compose down
sudo docker ps          # confirm all containers have stopped
sudo docker compose up -d
```

**Step 7 — Verify**

```bash
sudo docker ps          # both containers (streamlit_app, nginx) should be running
sudo docker compose ps  # check status and ports
```

**Step 8 — Test in browser**

Open `http://lee-edl.miserver.it.umich.edu` and confirm the new changes are live.

**Optional: Clean up old images**

```bash
sudo docker image prune -f
```

---

### Tips

- Always bump the image tag on every build (`0.0.1 → 0.0.2 → 0.0.3`). It makes rollbacks easy — just update the tag in `docker-compose.yml` and redeploy with an older image.
- The nginx config at `~/nginx/conf.d/streamlit.conf` rarely needs to change. It is mounted as a volume into the nginx container, so edits take effect after `docker compose restart nginx`.
- `.streamlit/config.toml` is baked into the Docker image at build time (via `git clone`). If you update the server address or port, commit the change and rebuild the image.
