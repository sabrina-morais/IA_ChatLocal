import os

from rag.pdf_reader import extract_text
from rag.vectorstore import add_document

PDF_FOLDER = "data/pdfs"


def ingest_all():

    total = 0

    files = os.listdir(PDF_FOLDER)

    for file in files:

        if file.lower().endswith(".pdf"):

            path = os.path.join(
                PDF_FOLDER,
                file
            )

            text = extract_text(path)

            add_document(
                text=text,
                source=file
            )

            total += 1

    return total