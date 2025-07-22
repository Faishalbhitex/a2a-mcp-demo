# Agent ADK Client

Agent ADK sebagai agent client untuk berkomunikasi dengan agent server atau agent remote yang tersedia

## Syarat
- Python 3.11=
- [uv package](https://docs.astral.sh/uv/getting-started/installation/)

## Metode jalankan
**asumsi anda sudah  masuk virtual enviroment dan sudah instal depedensi yang dibutuhkan tanya aja ke AI(gemini-claude rekomendasi karena dua model ini paham konteks dengan baik untuk uv) kalau kurang paham cara install uv, uv venv, masuk venv, uv sync dan uv run .**
**syarat** harus jalankan dulu agent server dan taruh url agent server sebelum  menjalankan agent ini karena koneksi harus manual tiap agentnya.
Ada dua mode menjalnkan ini bisa menggunakan  adk web untuk berjalan di web ui buatan adk dan di main.py untuk berinterasik di terminal.

1. ADK web:
**pastikan berada di dir `../adk_clinet/` ***
lalu jalankan di terminal di direktori tersebut
```bash
adk web  # di Windows jika adk web error bisa coba adk web --no-reload
```

2. Terminal Custom:
masuk ke `../adk_client/main.py` dan jalankan
```bash
uv run .
```
