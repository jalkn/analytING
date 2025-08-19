## analytING

This project implements a conversational agent, designed to answer questions related to customer master data, consumption, and field activities. The agent uses a **Retrieval-Augmented Generation (RAG)** approach with **LangGraph** to ground its answers in provided datasets. The solution is containerized using **Docker** and exposes a **REST API** via **FastAPI**.

### Key Components

* **`Dockerfile`**: A Dockerfile that creates a self-contained image. It installs all dependencies, copies the application code, and sets up the Uvicorn server to run the FastAPI application. The container is designed to run locally with no complex setup steps beyond `docker run`.
* **`chat/main.py`**: The entry point for the FastAPI application. This file defines the API endpoints and orchestrates the interaction with the conversational agent logic.
* **`chat/`**: This directory contains the core business logic of the agent.
    * **`agent_tools.py`**: Implements the functions (tools) that the LangGraph agent uses to query the provided datasets and the CREG Resolution 105 PDF. These tools are designed to answer questions about customer master data, consumption records, and field activities. The implementation includes the required joins for customer master and consumption data by `id_acuerdo`, and customer master and activities by `id_punto_servicio`.
    * **`rag_pipeline.py`**: Defines the LangGraph agent's architecture, including its state and the RAG pipeline. It integrates the LLM with the search and query tools to generate grounded responses.
* **`src/`**: This directory holds all the provided datasets in CSV format.
* **`assets/`**: This directory holds the CREG Resolution 105 PDF, which is used by the agent to answer regulatory questions.
* **`datos.sqlite`**: A SQLite database containing a copy of the provided datasets (customer master, consumption, and field activities).
* **`LLM_Connection.py`**: A module for securely managing and connecting to the external LLM endpoint using an API key from the environment variables.
* **`requirements.txt`**: This file lists all necessary Python dependencies for the project, including `langgraph`, `fastapi`, and `pypdf`, among others.

---

### Setup and Execution Instructions 

1. clone this repository
    ```bash
    git clone https://github.com/user/analytING.git
    ```
2.  Modify the .env file, adding your openai api key
3.  **Build and Run the Docker Container**: Once the `run.ps1` script completes, it will automatically build the Docker image and provide the final command to run the container. You must provide your OpenAI API key as an environment variable in the command.
    ```bash
    docker run -it --rm -e OPENAI_API_KEY="YOUR_API_KEY" -p 8000:8000 chatbot-app
    ```
4.  **Access the API**: The API will be available at `http://localhost:8000`. You can test the endpoints using a tool like Postman or `curl`. The agent is configured to answer in **Spanish** and will indicate the data source used for each response, including a tabular breakdown where applicable.

4. ### Querying the API

To query the API, you can use a `curl` command to send a POST request to the `/chat/` endpoint with your question in the `query` parameter. Make sure to URL-encode your question to handle spaces and special characters.

**Example using `curl`:**

To ask about the consumption of a customer named "Juan Perez", you would use the following command:

```bash
curl -X POST "http://localhost:8000/chat/?query=cual%20es%20el%20consumo%20de%20Juan%20Perez%3F" -H "accept: application/json"
```

To find the field activities for a customer with the ID d21ed, you can use this command:

```bash
curl -X POST "http://localhost:8000/chat/?query=Que%20actividades%20de%20campo%20se%20han%20realizado%20para%20el%20cliente%20con%20el%20ID%20de%20acuerdo%20d21ed%3F" -H "accept: application/json"
```


### File Structure 

```
/
├── .venv/
├── chat/
│   ├── agent_tools.py
│   ├── main.py
│   └── rag_pipeline.py
├── src/
│     ├── actividades_pruebas.csv 
│     ├── consumos_pruebas.csv        
│     ├── Energy_consumption_dataset.csv     
│     └── maestro_prueba.csv 
├── dockerfile
├── LLM_Connection.py
└── requirements.txt           

```# analytING
