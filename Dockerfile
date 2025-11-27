# ---- Base Image ----
FROM python:3.12-slim

# ---- Install System Dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---- Set Working Directory ----
WORKDIR /app

# ---- Copy Requirements ----
COPY requirements.txt .

# ---- Install Python Dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy Application Code ----
COPY src/ src/
COPY config/ config/
COPY data/ data/
COPY README.md .

# ---- Ensure Python Can Import Local Code ----
ENV PYTHONPATH="/app"

# ---- Expose FastAPI Port (for docker run -p mapping) ----
EXPOSE 8000

# ---- Default Command ----
CMD ["python3", "-m", "src.services.fastapi_backend.main"]
