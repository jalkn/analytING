import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_llm_client():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(
        api_key=api_key,
    )
    return client
