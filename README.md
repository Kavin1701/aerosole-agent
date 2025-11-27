# Aerosole Agent


## 🛠️ Quick Start

### Prerequisites
- Docker Desktop (or Docker engine) installed and running.
- Git installed for cloning the repository.

## Installation Guide (Docker)

### 1. Clone the Repository
```bash
git clone https://github.com/kavin-1digitals/aerosole-agent.git
cd aerosole-agent
```

### 2. Build the Docker Image
Ensure Docker is running, then build the image:
```bash
docker build -t aerosole-agent .
```

### 3. Run the Docker Container
Start the container, mapping port 8000:
```bash
docker run -p 8000:8000 aerosole-agent
```
- This maps the container's port 8000 to the host's port 8000.
- The FastAPI backend will start automatically.