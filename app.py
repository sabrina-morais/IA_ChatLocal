import os

from fastapi import FastAPI
from fastapi import Request
from fastapi import UploadFile
from fastapi import File

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from llm.ollama_client import ask_llm
from llm.ollama_client import history

from rag.ingest import ingest_all
from rag.vectorstore import search

app = FastAPI()

templates = Jinja2Templates(
    directory="templates"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/chat")
async def chat(data: dict):

    pergunta = data["message"]

    docs = search(pergunta)

    if docs:

        contexto = "\n".join(docs)

        prompt = f"""
Utilize o contexto abaixo.

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}
"""

    else:

        prompt = pergunta

    resposta = ask_llm(prompt)

    return {
        "response": resposta
    }


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    save_path = os.path.join(
        "data/pdfs",
        file.filename
    )

    with open(save_path, "wb") as f:

        f.write(await file.read())

    return {
        "message": f"{file.filename} carregado."
    }


@app.post("/ingest")
async def ingest():

    total = ingest_all()

    return {
        "message":
        f"{total} PDF(s) indexado(s)"
    }


@app.post("/clear")
async def clear():

    history.clear()

    return {
        "status": "ok"
    }