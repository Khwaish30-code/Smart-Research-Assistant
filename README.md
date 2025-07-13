# 🧠 Smart Research Assistant (RAG-based GenAI App)

This is a GenAI-powered assistant built using LangChain, ChromaDB, and LLaMA 3 (via Ollama) that helps users interact intelligently with uploaded PDF or TXT documents. It offers two modes:

- **Ask Anything**: Ask open-ended questions about the uploaded document.
- **Challenge Me**: Get quizzed with logic-based questions generated from the document and receive evaluation for your answers.

---

## ✅ Features

- 📄 Accepts both **PDF** and **TXT** files
- ⚡ Uses **LLaMA 3.2** (via **Ollama**) as the local LLM
- 🔍 Embeds and indexes content using **ChromaDB**
- 💬 Two interaction modes:
  - **Ask Anything**: Retrieval-Augmented QA
  - **Challenge Me**: Question generation + evaluation
- 🌐 Built with **Streamlit** for a clean web UI

---

## ⚙️ Setup Instructions

### 1. ✅ Install Python (3.10+ recommended)

Check Python version:
```bash
python --version
```

---

### 2. ✅ Create & activate a virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate      
```

---

### 3. ✅ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. ✅ Install and start **Ollama** (LLaMA engine)

- Download Ollama: https://ollama.com/download
- Pull LLaMA 3 model:
  ```bash
  ollama pull llama3
  ```
- Start the Ollama server:
  ```bash
  ollama serve
  ```

Leave this terminal running in the background.

---

### 5. ✅ Run the app

In a new terminal:

```bash
streamlit run app.py
```

The app will launch in your browser at:
```
http://localhost:8501
```

---

## 🧠 Architecture / Reasoning Flow
<pre> ```text ┌────────────────────────────┐ │ PDF / TXT Upload │ └────────────┬───────────────┘ │ ┌───────▼────────┐ │ Load & Split │ ←─ (LangChain loaders + text splitter) └───────┬────────┘ │ ┌───────▼────────┐ │ Embed Chunks │ ←─ sentence-transformers └───────┬────────┘ │ ┌───────▼────────┐ │ Store in Chroma│ ←─ Vector DB └───────┬────────┘ │ ┌────────▼─────────┐ │ Interaction │ ←─ Ask Anything / Challenge Me └────────┬─────────┘ │ ┌───────▼────────┐ │ LLaMA 3 │ ←─ via Ollama (local reasoning) └────────────────┘ ``` </pre>
