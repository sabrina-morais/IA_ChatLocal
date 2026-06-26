import os

from rag.pdf_reader import extract_text
from rag.audio_reader import transcribe_audio
from rag.chunker import chunk_text
from rag.video_converter import extract_audio
from rag.vectorstore import add_document

from config import PDF_FOLDER
from config import AUDIO_FOLDER
from config import VIDEO_FOLDER

def ingest_pdf():

    total = 0

    for file in os.listdir(PDF_FOLDER):

        if file.endswith(".pdf"):

            path = os.path.join(
                PDF_FOLDER,
                file
            )

            text = extract_text(path)

            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):

                add_document(
                    chunk,
                    f"{file}_{i}"
                )

            total += 1

    return total


def ingest_audio():

    total = 0

    for file in os.listdir(AUDIO_FOLDER):

        if file.endswith(
            (
                ".mp3",
                ".wav",
                ".m4a"
            )
        ):

            path = os.path.join(
                AUDIO_FOLDER,
                file
            )

            text = transcribe_audio(path)

            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):

                add_document(
                    chunk,
                    f"{file}_{i}"
                )

            total += 1

    return total


def ingest_video():

    total = 0

    for file in os.listdir(VIDEO_FOLDER):

        if file.endswith(".mp4"):

            path = os.path.join(
                VIDEO_FOLDER,
                file
            )

            audio_path = extract_audio(
                path
            )

            text = transcribe_audio(
                audio_path
            )

            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):

                add_document(
                    chunk,
                    f"{file}_{i}"
                )

            total += 1

    return total
