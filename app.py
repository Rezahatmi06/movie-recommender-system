import streamlit as st
import pickle
import pandas as pd

# 1. SETUP HALAMAN UI
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# 2. MUAT DATA (Hanya untuk mengisi Dropdown)
try:
    movies_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    movie_titles = movies['title'].values
except FileNotFoundError:
    # Error handling jika file belum ada, agar UI tetap jalan
    st.error("File 'movies.pkl' tidak ditemukan. Pastikan sudah menjalankan process_data.py")
    movie_titles = ["Avatar", "Titanic", "Avengers"] # Dummy data

# 3. HEADER & JUDUL
st.title('Gamafilm')
st.markdown("""
    <style>
    .big-font {
        font-size:18px !important;
        color: gray;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="big-font">Menggunakan Content-Based Filtering</p>', unsafe_allow_html=True)
st.write("---") 

# 4. INPUT PENGGUNA (DROPDOWN) 
st.subheader('Cari film yang Anda sukai:')
selected_movie_name = st.selectbox(
    'Ketik atau pilih judul film dari daftar:',
    movie_titles
)

# 5. TOMBOL AKSI
if st.button('Rekomendasikan Film'):
    
    st.write("---")
    st.subheader(f"Karena Anda menyukai '{selected_movie_name}', kami menyarankan:")
    
    # 6. LAYOUT KOLOM (UI HASIL) 
    # buat 5 kolom untuk menampilkan poster
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.image("https://via.placeholder.com/300x450?text=Poster+1", caption="Rekomendasi 1")
        st.write("**Judul Film 1**")
        
    with col2:
        st.image("https://via.placeholder.com/300x450?text=Poster+2", caption="Rekomendasi 2")
        st.write("**Judul Film 2**")

    with col3:
        st.image("https://via.placeholder.com/300x450?text=Poster+3", caption="Rekomendasi 3")
        st.write("**Judul Film 3**")

    with col4:
        st.image("https://via.placeholder.com/300x450?text=Poster+4", caption="Rekomendasi 4")
        st.write("**Judul Film 4**")

    with col5:
        st.image("https://via.placeholder.com/300x450?text=Poster+5", caption="Rekomendasi 5")
        st.write("**Judul Film 5**")

# --- FOOTER ---
st.write("---")
st.caption("Dibuat dengan Streamlit & TMDB API")