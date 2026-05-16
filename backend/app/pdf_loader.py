from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP

def load_and_split_pdf(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    print("DOCUMENTS LOADED:", len(documents))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300
    )

    chunks = splitter.split_documents(documents)

    print("CHUNKS CREATED:", len(chunks))

    print(chunks[0].page_content[:500])

    return chunks
# def load_and_split_pdf(pdf_path):

#     loader = PyPDFLoader(pdf_path)

#     documents = loader.load()

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=CHUNK_SIZE,
#         chunk_overlap=CHUNK_OVERLAP
#     )

#     chunks = splitter.split_documents(documents)

#     return chunks