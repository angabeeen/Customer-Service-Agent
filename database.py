# from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import openai 
from dotenv import load_dotenv
import os
import shutil
load_dotenv()

#openai.api_key = os.environ["API_KEY"]

CHROMA_PATH = "chroma"
DATA_PATH = "data/policy"

def main():
    setup_documents()

def setup_documents():
    documents=load_documents()
    chunks=split(documents)
    save_doc(chunks)

def load_documents():

    loader = DirectoryLoader(DATA_PATH, glob="**/*",loader_cls=TextLoader)
    documents=loader.load()
   
    return documents


def split(documents: list[Document]):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        add_start_index=True
        )

    
    chunks=splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[1]
    print(document.page_content)
    print(document.metadata)

    return chunks

def save_doc(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db=Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()

