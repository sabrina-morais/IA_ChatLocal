import os
import chromadb
import hashlib
from sentence_transformers import SentenceTransformer
from config import CHROMA_DB_PATH

os.environ[
    "ANONYMIZED_TELEMETRY"
] = "False"

# =====================================================
# ChromaDB
# =====================================================

client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH,
    
)

collection = client.get_or_create_collection(
    name="documents"
)

# =====================================================
# Embeddings
# =====================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =====================================================
# Adicionar documento
# =====================================================

def add_document(text, source):

    embedding = (
        embedding_model
        .encode(text)
        .tolist()
    )

    document_id = hashlib.md5(
        text.encode()
    ).hexdigest()

    collection.add(
        ids=[document_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[
            {
                "source": source
            }
        ]
    )


def search(
    query,
    n_results=5
):

    query_embedding = (
        embedding_model
        .encode(query)
        .tolist()
    )

    result = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=n_results
    )

    docs = []

    for i, doc in enumerate(
        result["documents"][0]
    ):

        docs.append(
            {
                "text": doc,
                "source":
                result["metadatas"][0][i][
                    "source"
                ]
            }
        )

    return docs


def stats():

    return {
        "documents":
        collection.count()
    }