import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langgraph.prebuilt.tool_executor import ToolInvocation
import json
import operator

class AgentState(TypedDict):
    query: str
    chat_history: Annotated[List[BaseMessage], operator.add]
    intermediate_steps: Annotated[List[BaseMessage], operator.add]
    final_answer: str

# Defining the nodes of the graph
def call_model(state, tools):
    """
    Node to invoke the LLM with the current query and history.
    """
    query = state['query']
    history = state.get('chat_history', [])
    intermediate_steps = state.get('intermediate_steps', [])
    
    # Creating the prompt for the LLM
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente conversacional útil diseñado para responder preguntas sobre datos de clientes, consumo y actividades de campo. Utiliza las herramientas disponibles para responder. Responde siempre en español. Si las herramientas no proporcionan la información, responde de manera cortés indicando que no tienes la información."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
        ("placeholder", "{intermediate_steps}")
    ])
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    chain = prompt | llm.bind_tools(tools)
    response = chain.invoke({
        "input": query, 
        "chat_history": history, 
        "intermediate_steps": intermediate_steps
    })
    
    return {"intermediate_steps": [response]}

def call_tool(state, tool_executor):
    """
    Node to execute the tool selected by the LLM.
    """
    tool_call = state['intermediate_steps'][-1].tool_calls[0]
    action = ToolInvocation(
        tool=tool_call.name,
        tool_input=tool_call.args
    )
    response = tool_executor.invoke(action)
    return {"intermediate_steps": [AIMessage(content=f"Tool output: {response}")]}


def should_continue(state):
    """
    Conditional edge to decide if the conversation should continue.
    """
    if state['intermediate_steps'][-1].tool_calls:
        return "continue"
    else:
        # Check if the last message is a final answer
        response_content = state['intermediate_steps'][-1].content
        if "Fuente: " in response_content or "No se pudo" in response_content:
            return "end"
        else:
            return "final_answer_node"

def final_answer_node(state):
    """
    Node to format the final answer.
    """
    final_response = state['intermediate_steps'][-1].content
    return {"final_answer": final_response}


def create_rag_pipeline(tools):
    """
    Defines the LangGraph agent's architecture.
    """
    tool_executor = ToolExecutor(tools)
    
    # Building the graph
    workflow = StateGraph(AgentState)
    
    # Adding nodes
    workflow.add_node("call_model", lambda state: call_model(state, tools))
    workflow.add_node("call_tool", lambda state: call_tool(state, tool_executor))
    workflow.add_node("final_answer_node", final_answer_node)

    # Setting up the entry point and edges
    workflow.set_entry_point("call_model")
    workflow.add_conditional_edges(
        "call_model",
        should_continue,
        {
            "continue": "call_tool",
            "end": END,
            "final_answer_node": "final_answer_node"
        }
    )
    workflow.add_edge("call_tool", "call_model")
    workflow.add_edge("final_answer_node", END)

    app = workflow.compile()
    return app

