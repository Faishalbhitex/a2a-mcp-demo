# 🧐 AI ADK Agent Server

Agent ADK sederhana menggunakan framework Google‑ADK dan tool Google Search.
Didesain sebagai template minimal untuk membuat agent AI berbasis Gemini.

---

## ⚙️ Fitur

* Integrasi dengan **Gemini API** (chat/LLM model).
* Mendukung query ke Google Search.
* Struktur modular untuk dikembangkan lebih lanjut.

---

## 📎 Prasyarat

* Python **3.11+**

* `uv` package manager (Astral UV)
  Perintah instalasi & dokumentasi: [uv Installation Docs](https://docs.astral.sh/uv/getting-started/installation/)

* **Gemini API key**
  Simpan di environment variable: `GEMINI_API_KEY=your_key_here`

---

## 🔧 Instalasi & Menjalankan

### 1. Clone Repo dan Masuk ke Direktori

```bash
git clone https://{host}/youruser/adk-agent.git
cd agents/adk_agent
```

### 2. Buat Virtual Environment (cross‑platform)

```bash
uv venv
```

### 3. Aktifkan Virtual Environment

**Windows**

```powershell
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
uv sync
```

### 5. Konfigurasi Gemini API

Tambahkan key ke environment:

**Windows** (PowerShell):

```powershell
setx GEMINI_API_KEY "your_key_here"
```

**Linux / macOS** (bash/zsh):

```bash
export GEMINI_API_KEY="your_key_here"
```

> 💡 Cek apakah sudah tersedia:
>
> ```bash
> echo $GEMINI_API_KEY    # Linux/Mac
> echo %GEMINI_API_KEY%   # Windows PowerShell
> ```

### 6. Jalankan Agent Server

```bash
uv run .
```

Server akan berjalan di `http://localhost:10001`

---