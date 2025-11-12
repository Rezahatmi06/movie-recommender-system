# Movie Recommender System 🎬

Sistem rekomendasi film sederhana menggunakan pendekatan Content-Based Filtering dengan dataset TMDB 5000 movies.

## Fitur
- Rekomendasi berdasarkan kesamaan Genre, Keywords, Cast, dan Director.
- UI interaktif menggunakan Streamlit.

## Cara Menjalankan (Local)

1. Clone repository ini.
2. Install library:
   pip install -r requirements.txt
3. Generate Model (Karena file .pkl tidak diupload):
   - Jalankan `python fetch_data.py` (Masukkan API Key TMDB Anda di script ini).
   - Jalankan `python process_data.py`.
4. Jalankan Aplikasi:
   streamlit run app.py
