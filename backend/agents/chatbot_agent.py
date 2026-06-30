from backend.utils.llm import get_llm
from backend.rag.retriever import retrieve_similar
import json

llm = get_llm()
CHAT_PROMPT = """
You are HireGen AI, an intelligent recruitment assistant.
You have access to candidate profiles from the vector store.

Recruiter's question: {question}

Relevant candidate information retrieved:
{context}

Answer the recruiter's question based on the candidate data above.
Be specific, mention candidate names, scores, and skills.
Keep your answer concise and helpful.
"""

def chat_with_recruiter(question: str, chat_history: list = []) -> str:
    # Retrieve relevant candidates from vector store
    results = retrieve_similar(question, top_k=3)

    if not results:
        return "No candidate data found. Please upload and analyze resumes first."

    # Build context from retrieved candidates
    context_parts = []
    for r in results:
        data = r["data"]
        # Remove internal keys
        clean = {k: v for k, v in data.items() if not k.startswith("_")}
        context_parts.append(json.dumps(clean, indent=2))

    context = "\n---\n".join(context_parts)

    prompt = CHAT_PROMPT.format(question=question, context=context)
    response = llm.invoke(prompt)
    return response