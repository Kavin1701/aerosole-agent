## 🛠️ Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/kavin-1digitals/aerosole-agent.git
```
```
cd aerosole-agent
```
### 2. Create a virtual environment
```bash
python3 -m venv .venv
```
### 3. Activate the virtual environment
macOS / Linux:
```bash
source .venv/bin/activate
```
Windows (PowerShell):
```bash
.venv\Scripts\activate
```
📦 Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the Project
Start the FastAPI backend:
```bash
python3 -m src.services.fastapi_backend.main
```
Your API will be available at:

👉 http://0.0.0.0:8000/docs

🧪 Test the Agent
Example request (via browser or API client):

```sql
GET /api/invoke_agent?query=search me casual shoes
```