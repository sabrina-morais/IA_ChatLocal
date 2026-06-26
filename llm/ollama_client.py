import requests

from config import MODEL_NAME
from config import OLLAMA_URL

history = []


def ask_llm(question):

    global history

    history.append({
        "role": "user",
        "content": question
    })

    payload = {
        "model": MODEL_NAME,
        "messages": history,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    data = response.json()

    answer = data["message"]["content"]

    history.append({
        "role": "assistant",
        "content": answer
    })

    return answer