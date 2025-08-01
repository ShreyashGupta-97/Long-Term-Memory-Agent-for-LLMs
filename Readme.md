# GPT Long-Term Memory Agent

## Project Purpose and Main Features

This project implements a **memory storage and retrieval agent** using OpenAI APIs, designed to give GPT models persistent long-term memory across conversations. The system records relevant "memories" from user inputs, efficiently storing them in a semantic vector store and retrieving them upon request.

### Key Features
- **Add Memories:** Extracts discrete facts from user messages and stores them as memories. Prevents duplication of information by accident
- **Retrieve Memories:** Answers user queries by retrieving relevant stored memories and synthesizing responses.
- **Delete Memories:** Removes specified memories when the user indicates they no longer apply. 
- **Multi-User/Session Support:** Configured to isolate memories by user/session.
- **Persistent Storage:** Linked with a vector database (Chroma) for durable storage of embeddings and facts.
- **Intent Classification:** Automatically infers user intent (add, retrieve, delete) from messages using GPT.
- **Safe Operations:** Prompts for confirmation before deleting memories to prevent accidental loss.

---

## Python Version & Dependencies

- **Python:** 3.11.9 (recommended)
- **Main dependencies:**
  - `openai`
  - `langchain`
  - `langchain_openai`
  - `chromadb` (for persistent vector storage)
  - `langchain_community`

## Setting Up the OpenAI API Key

To securely use OpenAI APIs, set it as an environment variable:

### Windows

Open the command prompt and type the following command
**Temporary (per session):**
set OPENAI_API_KEY=your_openai_api_key_here

**Permanent (persist across sessions):**
setx OPENAI_API_KEY "your_openai_api_key_here"
Then open a new Command Prompt window.

### Linux / macOS (bash/zsh)
export OPENAI_API_KEY="your_openai_api_key_here"

---

## Setting Up the Virtual Environment

1. Navigate to your project directory
2. Run the following commands on your terminal:
    ### Windows
    python -m venv .venv

    ### macOS/Linux
    python3 -m venv .venv

    Replace .venv with whatever you want to name your environment

3. Activate the Virtual Environment
    ### Windows
    .venv\Scripts\activate

    ### macOS/Linux
    source .venv/bin/activate

    When your environment is activated, your shell prompt will show the environment name

4. Deactivate when done using the following command:
    deactivate


## Running the Script

1. Clone or download this repository.
2. Ensure you have Python 3.11.9 installed.
3. Setup and activate the virtual environment as described above
3. Install dependencies:
    pip install -r requirements.txt
4. Set your OpenAI API key as described above.
5. Run the script:
    python main.py
6. Interact with the agent via the command line:
    - Add memories by telling the agent facts (e.g., “I use Shram and Magnet as productivity tools”).
    - Retrieve memories by asking questions (e.g., “What are the productivity tools that I use?”).
    - Delete memories by commands like “I don't use Magnet anymore”.
7. Type `exit` to quit the program.

---

## Additional Information

- The project uses **Chroma** vector database with an option for **persistent local storage**—memories are saved on disk and remain available across restarts.
- The system uses GPT-4 (or another OpenAI model you configure) for intent classification, fact extraction, and response generation.
- Information that is already stored in the memory is prevented from being added again, thus, avoiding duplication.
- Confirmations are implemented for critical operations like deletion to avoid accidental loss.
- For multi-user support, the project can be extended to isolate memories per user by associating vectorstore collections and chat history with a user/session ID.
- The agent assumes a conversational interface (CLI by default), but can be integrated into other frontends.

---

## Troubleshooting

- If the API key is not set or incorrectly set, the script will raise an error prompting you to set `OPENAI_API_KEY`.
- On Windows, remember to open a new CMD window after using `setx` for environment variables to take effect.
- If you encounter errors related to dependencies, verify correct installation and compatible versions.
- For any semantic similarity issues or unexpected memory retrieval behavior, adjusting similarity thresholds or tuning prompts may help.

---

## Deployment Strategies

This project can be easily deployed as a RESTful API service using **FastAPI**. This FastAPI deployment enables us to turn the memory agent into a scalable, modern microservice accessible from anywhere via HTTP.

#### 1. **Wrap the Core Logic as FastAPI Endpoints**

- Expose endpoints for memory operations such as:
  - `/add_memory` (POST): Accepts user facts and stores them.
  - `/retrieve_memory` (GET/POST): Accepts user queries and returns answers based on stored memories.
  - `/delete_memory` (POST): Removes specified memories after user confirmation.
- Each endpoint parses JSON input and returns JSON responses, enabling easy frontend or integrations.

#### 2. **Asynchronous Processing**

- FastAPI supports `async def` endpoints, which can be leveraged especially if your operations (such as API calls to OpenAI) can be made asynchronously, increasing throughput and responsiveness.

#### 3. **Deployment with Gunicorn**

- Use Gunicorn with multiple workers for scalable deployment
- Endpoints can be protected with authentication (e.g., API keys, OAuth2) for multi-user environments.

#### 4. **Dockerization**

For portability and ease of deployment:
- Create a `Dockerfile` to containerize your FastAPI app.
- Build and run your Docker image anywhere, including cloud platforms.

#### 5. **Persistence and Scaling**

- The vector store (Chroma) data directory (`persist_directory`) should be mounted to a persistent volume in Docker/cloud deployments so that memories are not lost on each redeploy.
- For scaling across multiple servers, use a shared/persistent vector database or object storage backend.
- Deploy on a cloud platform (eg. AWS ECS, Kubernetes) with auto-scaling to handle traffic spikes. Use a load balancer to distribute requests.
- Cache frequent queries in Redis to reduce redundant memory retrieval computations.
- Monitoring: Use Prometheus and Grafana to monitor API latency, error rates, and query performance.

#### 6. **Environment Variables**

- Set sensitive environment variables (such as `OPENAI_API_KEY`) in your deployment environment/container, not in code.

## Way Forward
1. Memory updation logic can be implemented. This can be done by creating a separate function and adding a new intent 'update_memory'. If this intent is detected, the old fact is deleted and the new fact is added in the vector store. However, this can have potential issues of removing some important information.
2. The memory retrieval can be enhanced by summarizing the information
3. Text-to-Speech and Speech-to-Text engines can be integrated to make the system accessible to specially-challenged people.


Thank you for using the GPT Long-Term Memory Agent project!