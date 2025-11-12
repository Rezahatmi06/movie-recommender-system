import requests
import pickle
import time
import os  # Kita butuh 'os' untuk mengecek apakah file ada
from tqdm import tqdm

# --- KONFIGURASI ---
API_KEY = '0c04259b81c1b4beafa9ddee8a225f8e'
BASE_URL = 'https://api.themoviedb.org/3'
# File untuk menyimpan hasil
OUTPUT_FILE = 'movies_data.pkl'

# --- 1. MENGAMBIL 5000 ID FILM (dari 250 Halaman) ---
# (Bagian ini sama persis, karena cepat dan tidak masalah jika diulang)

print("Memulai Tahap 1: Mengambil 5000 ID film...")
movie_ids = []
# Loop dari halaman 1 sampai 250
for page in tqdm(range(1, 251), desc="Mengambil halaman"):
    url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=en-US&page={page}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        page_ids = [movie['id'] for movie in data['results']]
        movie_ids.extend(page_ids)
    except requests.exceptions.RequestException as e:
        print(f"Error di halaman {page}: {e}")
        continue
    time.sleep(0.1) 

print(f"Tahap 1 Selesai. Total {len(movie_ids)} ID unik ditemukan.")
unique_ids = list(set(movie_ids)) 

# --- 2. PERSIAPAN SEBELUM DOWNLOAD DETAIL ---
# (Di sinilah perubahannya dimulai)

all_movie_data = []
downloaded_ids = set() # Gunakan 'set' agar pencarian cepat

# Cek apakah file output sudah ada
if os.path.exists(OUTPUT_FILE):
    print(f"Menemukan file lama: {OUTPUT_FILE}. Memuat data yang sudah ada...")
    try:
        with open(OUTPUT_FILE, 'rb') as f:
            all_movie_data = pickle.load(f)
        # Buat daftar ID yang sudah di-download
        for movie in all_movie_data:
            downloaded_ids.add(movie['id'])
        print(f"Berhasil memuat {len(all_movie_data)} data film yang sudah ada.")
    except Exception as e:
        print(f"Error saat memuat file {OUTPUT_FILE}: {e}. Memulai dari awal.")
        all_movie_data = []
        downloaded_ids = set()

# --- 3. MENGAMBIL DETAIL UNTUK SETIAP FILM (DENGAN CHECKPOINT) ---

print(f"\nMemulai Tahap 2: Mengambil detail film (Total {len(unique_ids)} film)...")

# Loop untuk setiap ID film yang unik
for movie_id in tqdm(unique_ids, desc="Mengambil detail film"):
    
    # PERIKSA DI SINI: Jika ID sudah ada, lewati
    if movie_id in downloaded_ids:
        continue # Lanjut ke ID berikutnya

    # Jika belum ada, baru kita download
    try:
        # 1. Ambil Detail Utama (overview, genres)
        details_url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        details_response = requests.get(details_url)
        details_response.raise_for_status()
        details_data = details_response.json()

        # 2. Ambil Kredit (cast, crew)
        credits_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US"
        credits_response = requests.get(credits_url)
        credits_response.raise_for_status()
        credits_data = credits_response.json()
        
        # 3. Ambil Keywords
        keywords_url = f"{BASE_URL}/movie/{movie_id}/keywords?api_key={API_KEY}"
        keywords_response = requests.get(keywords_url)
        keywords_response.raise_for_status()
        keywords_data = keywords_response.json()

        # Gabungkan semua data yang kita perlukan
        movie_record = {
            'id': details_data['id'],
            'title': details_data['title'],
            'overview': details_data['overview'],
            'genres': details_data['genres'],
            'cast': credits_data['cast'],
            'crew': credits_data['crew'],
            'keywords': keywords_data['keywords'] 
        }
        
        all_movie_data.append(movie_record)
        downloaded_ids.add(movie_id) # Tandai sebagai sudah di-download

        # SIMPAN PROGRES SECARA BERKALA (setiap 50 film)
        if len(all_movie_data) % 50 == 0:
            with open(OUTPUT_FILE, 'wb') as f:
                pickle.dump(all_movie_data, f)
        
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil data untuk ID {movie_id}: {e}. (Akan dicoba lagi nanti)")
        continue # Lanjut ke ID berikutnya jika ada error

    time.sleep(0.1) # Tetap beri jeda

# --- 4. SIMPAN HASIL AKHIR ---
print(f"\nTahap 2 Selesai. Total film yang di-download sekarang: {len(all_movie_data)}.")
print(f"Menyimpan hasil akhir ke {OUTPUT_FILE}...")

with open(OUTPUT_FILE, 'wb') as f:
    pickle.dump(all_movie_data, f)

print(f"SELESAI! Data telah disimpan di {OUTPUT_FILE}.")