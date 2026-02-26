# 🛡️ AI Auditor Pro - RAG ISO 9001

Asistente inteligente basado en IA Local para la auditoría de Sistemas de Gestión de Calidad (ISO 9001:2015).

## 🚀 Características
- **Privacidad Total:** Los documentos nunca salen del equipo local (Uso de Ollama).
- **Arquitectura RAG:** Recuperación de información precisa mediante búsqueda semántica.
- **Modelos:** `nomic-embed-text` para embeddings y `gpt-oss` para generación.
- **Tecnologías:** LangChain (LCEL), FAISS, Python 3.14.

## 🛠️ Instalación
1. Clonar el repo.
2. Crear entorno virtual: `python -m venv .venv`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar ingesta: `python src/ingest.py`
5. Consultar: `python src/query.py`