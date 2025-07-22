# AI ADK Agent Host

Berinteraksi dengan agent server dengan ui gradio.

## Instalasi dan Menjalankan

### Prasyarat

* Python 3.11+
* uv package manager
* Instal uv jika belum punya di link ini [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Langkah-langkah

1. Navigasi ke direktori client

```bash
cd hosts/cli
```

2. Buat virtual environment

```bash
uv venv
```

3. Aktifkan virtual environment

* Windows:

```bash
.venv\Scripts\activate
```

* Linux/Mac:

```bash
source .venv/bin/activate
```

4. Instal dan sinkronisasi dependensi

```bash
uv sync
```

5. Jalankan agent client

```bash
uv run .
```
