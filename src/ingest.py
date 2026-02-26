import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

def ejecutar_ingesta():
    pdf_path = "docs/NOM_ISO_9001-2015.pdf"
    db_dir = "faiss_index" # Cambiamos el nombre de la carpeta

    if not os.path.exists(pdf_path):
        print(f"❌ No encuentro el archivo: {pdf_path}")
        return

    print(f"🚀 Iniciando proceso para: {pdf_path}")

    # 1. Cargar y dividir
    loader = PyPDFLoader(pdf_path)
    documentos = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documentos)
    
    print(f"✂️ Texto dividido en {len(chunks)} fragmentos.")

    # 2. Crear memoria con Ollama
    print("🧠 Generando memoria vectorial con Nomic-Embed-Text (FAISS)...")
    # Cambiamos gpt-oss por el modelo especializado en embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    try:
        vector_db = FAISS.from_documents(chunks, embeddings)
        vector_db.save_local(db_dir)
        print(f"✅ ¡Éxito! Memoria guardada en la carpeta '{db_dir}'.")
    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    ejecutar_ingesta()