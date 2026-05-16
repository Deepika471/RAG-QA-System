import os

from langchain_community.vectorstores import Chroma

from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import CHROMA_DB_DIR


os.makedirs(CHROMA_DB_DIR, exist_ok=True)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_store(chunks):

    print("INDEXING CHUNKS:", len(chunks))

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )

    vectorstore.persist()

    print("VECTOR STORE CREATED")

    return vectorstore


def load_vector_store():

    print("LOADING DB FROM:", CHROMA_DB_DIR)

    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )

    return vectorstore