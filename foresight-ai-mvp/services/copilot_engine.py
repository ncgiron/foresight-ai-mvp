import json
import requests

OLLAMA_URL = "http://192.168.8.163:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def build_prompt(question: str, context: dict):

    context_json = json.dumps(
        context,
        indent=2
    )

    return f"""
You are a senior telecom packet core engineer.

Use ONLY the information in the network context.

Network Context:
{context_json}

Question:
{question}

Provide:
1. Summary
2. Findings
3. Recommendations

Answer:
"""


def ask_llm(question: str, context: dict):

    prompt = build_prompt(
        question,
        context
    )

    print(f"Calling Ollama: {OLLAMA_URL}")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]