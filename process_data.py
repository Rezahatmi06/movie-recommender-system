import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- FUNGSI BANTUAN UNTUK PREPROCESSING ---

# Fungsi 1: Mengambil nama dari format dictionary (untuk Genre & Keywords)
def convert(obj):
    L = []
    for i in obj:
        L.append(i['name']) 
    return L

# Fungsi 2: Mengambil 3 aktor teratas saja
def convert3(obj):
    L = []
    counter = 0
    for i in obj:
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

# Fungsi 3: Mencari Sutradara
def fetch_director(obj):
    L = []
    for i in obj:
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

# Fungsi 4: Menghilangkan Spasi (PENTING)
# Mengubah 'Sam Worthington' menjadi 'SamWorthington'
# Agar sistem tidak bingung antara 'Sam Worthington' dan 'Sam Mendes'
def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

# --- LANGKAH 3: PREPROCESSING ---
print("1. Memuat data mentah...")
movies_dict = pickle.load(open('movies_data.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

print("2. Membersihkan data (ini mungkin butuh waktu sebentar)...")

# Ekstraksi Genre dan Keywords
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# Ekstraksi 3 Aktor Utama
movies['cast'] = movies['cast'].apply(convert3)

# Ekstraksi Sutradara
movies['crew'] = movies['crew'].apply(fetch_director)

# Pecah Sinopsis (Overview) menjadi list kata
# Kita perlu handle jika ada data kosong (NaN)
movies['overview'] = movies['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])

# Menghilangkan spasi pada nama dan genre
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)
movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)

# MEMBUAT KOLOM 'TAGS' (GABUNGAN SEMUANYA)
print("3. Membuat Tags...")
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Buat DataFrame baru yang lebih bersih (hanya ID, Judul, dan Tags)
new_df = movies[['id', 'title', 'tags']].copy()

# Gabungkan list tags menjadi kalimat string dan ubah ke huruf kecil
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

print("   Contoh tags data pertama:")
print(f"   {new_df['tags'][0]}")

# --- LANGKAH 3 (LANJUTAN): VEKTORISASI ---
print("\n4. Melakukan Vektorisasi (CountVectorizer)...")
# max_features=5000 artinya kita hanya mengambil 5000 kata paling sering muncul
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

print(f"   Ukuran Matriks Vektor: {vectors.shape}")


# --- LANGKAH 4: MENGHITUNG KEMIRIPAN ---
print("\n5. Menghitung Cosine Similarity (Ini intinya!)...")
similarity = cosine_similarity(vectors)

print(f"   Ukuran Matriks Similarity: {similarity.shape}")


# --- LANGKAH 5: MENYIMPAN MODEL ---
print("\n6. Menyimpan file untuk Aplikasi...")

# Simpan DataFrame film (bersih)
pickle.dump(new_df, open('movies.pkl', 'wb'))

# Simpan Matriks Kemiripan
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("SELESAI! File 'movies.pkl' dan 'similarity.pkl' siap digunakan di Streamlit.")