# Aerosole Agent
## 🛠️ Quick Start
### Prerequisites
- Docker Desktop (or Docker engine) installed and running.
- Git installed for cloning the repository.
- OpenAI and Groq API keys (for LLM integrations).

## Installation Guide (Docker)
### 1. Clone the Repository
```bash
git clone https://github.com/Kavin1701/aerosole-agent.git
cd aerosole-agent
```

### 2. Set Up Environment Variables
Create a `.env` file for the LangGraph agent in the `config` folder to store your API keys:
- Navigate to the `config` folder: `cd config`.
- Create a file named `langgraph_agent.env` (or edit if it exists) and add the following:
  ```
  OPENAI_API_KEY=your_openai_api_key_here
  GROQ_API_KEY=your_groq_api_key_here
  ```
- Replace `your_openai_api_key_here` and `your_groq_api_key_here` with your actual API keys.
- Return to the project root: `cd ..`.

**Note:** These keys are required for the agent to function with OpenAI and Groq LLMs. Ensure the file is not committed to version control (add it to `.gitignore` if needed for security).

### 3. Build the Docker Image
Ensure Docker is running, then build the image:
```bash
docker build -t aerosole-agent .
```

### 4. Run the Docker Container
Start the container, mapping port 8000:
```bash
docker run -p 8000:8000 aerosole-agent
```
- This maps the container's port 8000 to the host's port 8000.
- The FastAPI backend will start automatically.

Once running, access the agent at `http://localhost:8000`. For more details, check the repository's README or API docs.