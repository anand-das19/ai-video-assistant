import os
import uuid
import tempfile
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
_embeddings_instance = None

def get_embeddings():
    """Singleton getter for HuggingFace embeddings model to conserve memory."""
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"}
        )
    return _embeddings_instance

def build_vector_store(transcript: str, collection_name: str = None, persist_dir: str = None) -> Chroma:
    """
    Build a Chroma vector store for the provided transcript.
    Uses a unique collection name and isolated temporary directory per session
    so multiple visitors do not collide.
    """
    print("Building vector store...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(transcript)

    docs = [
        Document(page_content=chunk, metadata={'chunk_index': i})
        for i, chunk in enumerate(chunks)
    ]

    session_id = uuid.uuid4().hex[:12]
    if collection_name is None:
        collection_name = f"meeting_{session_id}"
    if persist_dir is None:
        persist_dir = os.path.join(tempfile.gettempdir(), f"chroma_{session_id}")
        os.makedirs(persist_dir, exist_ok=True)

    embeddings = get_embeddings()
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_dir
    )

    return vector_store

def load_vector_store(collection_name: str = "meeting_transcript", persist_dir: str = "vector_db") -> Chroma:
    embeddings = get_embeddings()
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir
    )
    return vector_store

def get_retriever(vector_store: Chroma, k: int = 4):
    return vector_store.as_retriever(
        search_type='similarity',
        search_kwargs={"k": k}
    )
