import os
from openai import OpenAI
from dotenv import load_dotenv

_client_instance = None

def get_openai_client():
    global _client_instance
    if _client_instance is None:
        load_dotenv()
        api_key = os.getenv("APIKEY")
        _client_instance = OpenAI(api_key=api_key)
    return _client_instance