# Docker Deployment Guide

### 1. Prerequisites

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Make sure Docker Engine is running

### 2. Project Structure (Relevant Parts)

```
cheaper/
├── cheaper/
│   └── wsgi.py
├── environment.yml
├── Dockerfile
├── .dockerignore
├── main.py
├── setup.py
└── ...
```

---

### 3. Dockerfile

We're using Miniconda and `environment.yml` (not `requirements.txt`) for dependency management.

```dockerfile
FROM continuumio/miniconda3:latest

WORKDIR /app

COPY environment.yml .

RUN conda install -n base -c conda-forge mamba && \
    mamba env update -n base -f environment.yml && \
    conda clean --all --yes

COPY . .

# ⏱️ Gunicorn timeout is increased to handle long scraping time
CMD ["gunicorn", "--timeout", "120", "cheaper.wsgi:application", "-b", "0.0.0.0:8000"]
```

---

### 4. .dockerignore

```dockerignore
__pycache__/
*.pyc
*.pyo
*.pyd
env/
venv/
.git
```

---

### 5. Build and Run

```bash
# Build the Docker image
docker build -t cheaper-app .

# Run the container on port 8000
docker run --rm -p 8000:8000 cheaper-app
```

Open [http://localhost:8000](http://localhost:8000) — you should see:

```
Scraping complete.
```

---
