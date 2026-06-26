import os

from fastapi import FastAPI
from fastapi import Request
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException

from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from llm.ollama_client import ask_llm
from llm.ollama_client import history

from rag.vectorstore import search
from rag.vectorstore import stats

from rag.ingest import ingest_pdf
from rag.ingest import ingest_audio
from rag.ingest import ingest_video

from config import PDF_FOLDER
from config import AUDIO_FOLDER
from config import VIDEO_FOLDER


app = FastAPI()

templates = Jinja2Templates(
    directory="templates"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/chat")
async def chat(data: dict):

    pergunta = data.get(
        "message",
        ""
    )

    docs = search(pergunta)

    if docs:

        contexto = "\n\n".join(
            [
                doc["text"]
                for doc in docs
            ]
        )

    else:

        contexto = ""

    prompt = f"""
Você é um assistente inteligente.

Use o contexto abaixo quando ele
for relevante.

Se a resposta não estiver no contexto,
responda normalmente.

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}
"""

    resposta = ask_llm(prompt)

    return {
        "response": resposta
    }

@app.post("/clear")
async def clear_chat():

    history.clear()

    return {
        "success": True
    }


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    path = os.path.join(
        PDF_FOLDER,
        file.filename
    )

    with open(path, "wb") as f:
        f.write(await file.read())

    return {
        "success": True,
        "message": f"PDF enviado: {file.filename}"
    }


@app.post("/upload-audio")
async def upload_audio(
    file: UploadFile = File(...)
):

    path = os.path.join(
        AUDIO_FOLDER,
        file.filename
    )

    with open(path, "wb") as f:
        f.write(await file.read())

    return {
        "success": True,
        "message": f"Áudio enviado: {file.filename}"
    }


@app.post("/upload-video")
async def upload_video(
    file: UploadFile = File(...)
):

    path = os.path.join(
        VIDEO_FOLDER,
        file.filename
    )

    with open(path, "wb") as f:
        f.write(await file.read())

    return {
        "success": True,
        "message": f"Vídeo enviado: {file.filename}"
    }


@app.post("/ingest")
async def ingest():

    total = 0

    total += ingest_pdf()
    total += ingest_audio()
    total += ingest_video()

    return {
        "success": True,
        "message": f"{total} arquivos indexados."
    }

@app.get("/status")
async def status():

    return {
        "model": "qwen3:8b",
        "documents":
        stats()["documents"]
    }

from fastapi import HTTPException


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if not file.filename.endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Arquivo inválido."
        )

    path = os.path.join(
        PDF_FOLDER,
        file.filename
    )

    with open(path, "wb") as f:

        f.write(
            await file.read()
        )

    return {
        "success": True,
        "message":
        f"{file.filename} enviado."
    }