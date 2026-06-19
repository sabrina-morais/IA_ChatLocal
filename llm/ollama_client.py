import requests

MODEL = "qwen3:8b"

OLLAMA_URL = "http://localhost:11434/api/chat"

history = []


def ask_llm(prompt):

    global history

    history.append({
        "role": "user",
        "content": prompt
    })

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": history,
            "stream": False
        },
        timeout=300
    )

    data = response.json()

    answer = data["message"]["content"]

    history.append({
        "role": "assistant",
        "content": answer
    })

    return answer