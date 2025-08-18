from fastapi import FastAPI
from langchain_core.messages import AIMessage, HumanMessage
import uvicorn
import os
from dotenv import load_dotenv
from chat.rag_pipeline import create_rag_pipeline
from chat.agent_tools import get_all_tools
from LLM_Connection import get_llm_client

load_dotenv()

app = FastAPI(
    title="Conversational Agent API",
    description="A conversational agent using LangGraph and RAG.",
    version="1.0"
)

# Initialize the agent outside the endpoint for efficiency
try:
    llm_client = get_llm_client()
    tools = get_all_tools()
    agent = create_rag_pipeline(tools)
except ValueError as e:
    print(f"Failed to initialize agent: {e}")
    agent = None

@app.post("/chat/")
async def chat_endpoint(query: str):
    """
    Endpoint to interact with the conversational agent.
    """
    if not agent:
        return {"response": "Error: Agent not initialized. Check API key."}

    input_message = {"query": query, "chat_history": [], "intermediate_steps": []}
    response = agent.invoke(input_message)
    
    # Extracting the final answer from the agent's response
    final_answer = response.get("final_answer", "No se pudo generar una respuesta. Por favor, reformula la pregunta.")
    
    return {"response": final_answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

