import json
import requests

# OLLAMA_URL = "http://192.168.8.163:11434/api/generate" 
OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen2.5:3b"


def build_prompt(question: str, context: dict):

    root = context.get("root_cause", {})

    return f"""
You are a Telecom AI Copilot.

IMPORTANT NETWORK FACTS

Network Status:
{context.get("network_status")}

Root Cause:
{root.get("root_cause")}

Diagnosis:
{root.get("diagnosis")}

Evidence:
{root.get("evidence")}

Recommendation:
{root.get("recommendation")}

User Question:
{question}


RULES

- Always answer in English.
- Use the network facts above.
- If root cause is identified, do NOT say the network is healthy.
- Explain the root cause.
- If the user asks about network health, summarize the current status, root cause, evidence, and recommendation.
- Keep the answer concise and factual.

Answer:
"""

def ask_llm(question: str, context: dict):

    prompt = build_prompt(
        question,
        context
    )

    print(f"Calling Ollama: {OLLAMA_URL}")
    print("=" * 80)
    print(f"PROMPT LENGTH: {len(prompt)}")
    print("=" * 80)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=600
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]

    except requests.exceptions.Timeout:
        return "AI analysis timed out while waiting for Ollama."

    except Exception as e:
        return f"AI error: {str(e)}"