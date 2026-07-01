import os

USE_GROQ = os.getenv("USE_GROQ", "false").lower() == "true"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

def get_llm():
    """Returns a unified LLM that always outputs plain strings."""
    if USE_GROQ and GROQ_API_KEY:
        from langchain_groq import ChatGroq
        from langchain_core.output_parsers import StrOutputParser
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=GROQ_API_KEY,
            temperature=0.3
        )
        # Chain with StrOutputParser so output is always a plain string
        return llm | StrOutputParser()
    else:
        from langchain_ollama import OllamaLLM
        return OllamaLLM(model="llama3.2")