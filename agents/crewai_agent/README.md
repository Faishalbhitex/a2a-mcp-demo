# CrewAI Agent

CrewAI Agent ini adalah implementasi dari agen AI berbasis [CrewAI Framework](https://docs.crewai.com/en/introduction) yang dapat digunakan di dalam sistem A2A.

## Fitur

* Menggunakan LLM dari Google (Gemini) atau OpenAI (GPT-4o)
* Menggunakan Serper API sebagai alat pencarian informasi
* Terintegrasi dengan server A2A

## Prasyarat

Pastikan Anda sudah mengatur API key di file `.env`:

```
GOOGLE_API_KEY=...        # atau
OPENAI_API_KEY=...
SERPER_API_KEY=...
```

## Instalasi

Jalankan perintah berikut dari direktori `agents/crewai_agent`:

```bash
uv venv
source .venv/bin/activate   # atau .venv\Scripts\activate di Windows
uv sync
```

> File `pyproject.toml` dan `uv.lock` sudah tersedia.

## Menjalankan Agen

```bash
uv run .
```

Secara default akan berjalan di `http://localhost:10002/`

## Contoh Pertanyaan yang Didukung

* "Apa itu CrewAI dan bagaimana memulai?"
* "Bagaimana cara membuat beberapa agents dalam CrewAI?"
* "Apa perbedaan agent dan crew di CrewAI?"

## Catatan

* Agen ini hanya menjawab pertanyaan terkait CrewAI.
* Pertanyaan di luar domain seperti LangChain atau AutoGen akan ditolak secara sopan.

---

Untuk informasi selengkapnya tentang CrewAI, kunjungi: [https://docs.crewai.com/en/introduction](https://docs.crewai.com/en/introduction)
