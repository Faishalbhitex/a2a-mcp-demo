# LangGraph Agent Server

Agent AI sederhana berbasis framework **LangGraph** dan **LangChain** untuk menjawab pertanyaan seputar ekosistem LangChain (LangGraph, LangSmith, LangFlow).

---

## ✅ Prasyarat

* Python 3.11+
* [uv](https://docs.astral.sh/uv/getting-started/installation/) (package manager)
* API Key:

  * `GOOGLE_API_KEY` (untuk Gemini)
  * atau `TAVILY_API_KEY` (opsional, untuk tool search)

---

## 🚀 Instalasi & Menjalankan Server

### 1. Pindah ke direktori agent

```bash
cd agents/langgraph_agent
```

### 2. Buat dan aktifkan virtual environment

```bash
uv venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Sinkronisasi dependensi

```bash
uv sync
```

### 4. Siapkan API key di `.env`

Contoh isi file `.env`:

```
GOOGLE_API_KEY=isi_dengan_api_key_anda
TAVILY_API_KEY=opsional_jika_ingin_tools_search
```

### 5. Jalankan server agent

```bash
uv run .
```

Server akan berjalan di:

```
http://localhost:10003/
```

---

## 📌 Catatan

* Agent ini hanya fokus menjawab pertanyaan tentang LangChain, LangGraph, LangSmith, dan LangFlow.
* Gunakan dengan API key Gemini (Google) agar dapat bekerja dengan baik.

---