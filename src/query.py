import os
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Evitar advertencias innecesarias
os.environ["USER_AGENT"] = "AI-Auditor-Pro/1.0"

def consultar_auditor():
    db_dir = "faiss_index"
    
    # 1. Configuración de modelos
    print("🧠 Conectando con los modelos locales...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    llm = OllamaLLM(model="gpt-oss", streaming=True)

    # 2. Cargar la base de datos vectorial
    print("📂 Cargando base de datos de auditoría...")
    if not os.path.exists(db_dir):
        print(f"❌ Error: No existe la carpeta '{db_dir}'. Ejecuta primero 'python src/ingest.py'.")
        return
        
    vector_db = FAISS.load_local(db_dir, embeddings, allow_dangerous_deserialization=True)
    # 1. Aumentamos a 6 fragmentos para no perdernos nada
    retriever = vector_db.as_retriever(search_kwargs={"k": 6})

    # 2. Mejoramos el Prompt para que sea un poco más flexible
    template = """Eres un Auditor Senior de Sistemas de Gestión de Calidad.
    Tu objetivo es ayudar a Manuel a entender la norma ISO 9001:2015.

    Utiliza los siguientes fragmentos de la norma para responder. 
    Si el tema aparece mencionado pero no está el detalle completo, resume lo que veas.

    Contexto:
    {context}

    Pregunta: {question}

    Respuesta del Auditor (basada en el texto):"""

    prompt = ChatPromptTemplate.from_template(template)

    # 4. Construir la cadena moderna (LCEL)
    # Explicación: Buscamos contexto -> Pasamos la pregunta -> Aplicamos el Prompt -> Ejecutamos LLM -> Limpiamos texto
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("\n✅ SISTEMA DE AUDITORÍA LISTO")
    print("---------------------------------")
    
    while True:
        user_input = input("\nPregunta sobre la norma (o escribe 'salir'): ")
        if user_input.lower() in ['salir', 'exit', 'quit']:
            break
        
        print("🔍 Analizando normativa...")
        try:
            # En LCEL usamos invoke directamente
            respuesta = chain.invoke(user_input)
            print(f"\n🤖 AUDITOR:\n{respuesta}")
        except Exception as e:
            print(f"❌ Error en la consulta: {e}")

if __name__ == "__main__":
    consultar_auditor()