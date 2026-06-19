import chromadb

from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_or_create_collection(
    name="documents"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def add_document(text, source):

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[source],
        documents=[text],
        embeddings=[embedding]
    )


def search(query):

    embedding = model.encode(query).tolist()

    result = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    if result["documents"]:

        return result["documents"][0]

    return []