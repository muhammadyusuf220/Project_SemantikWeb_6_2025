import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import re
import requests

# Custom CSS untuk styling yang menarik
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        padding-top: 2rem;
        background: linear-gradient(135deg, #000000 0%, #062F4F 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom font */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #34495e, #2c3e50);
        color: white;
    }
    
    .sidebar-content {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 0.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Card styling */
    .info-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #813772 0%, #B82601 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }

    
    .feature-card:hover {
        transform: scale(1.05);
    }
    
    /* Search section styling */
    .search-section {
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        background: linear-gradient(180deg, #34495e, #2c3e50);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #B82601 0%, #813772 100%);
        color: white;
        border: none;
        width: auto !important;
        min-width: unset !important;
        border-radius: 25px;
        white-space: nowrap;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Status indicators */
    .status-connected {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .status-disconnected {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
        /* Perbesar ukuran isi tabel */
    iframe[data-testid="stDataFrame"] {
        zoom: 3;  /* Skala 1.2x dari ukuran default */
        min-height: 500px !important;
    }

    /* Perbesar font pada isi tabel */
    div[data-testid="stDataFrame"] iframe {
        zoom: 1.2;  /* skala 1.2x dari default */
    }

    
    /* Metrics styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
        /* === Sidebar background === */
    section[data-testid="stSidebar"] {
        background: #062F4F;
        color: white;
    }

    /* === Judul Navigasi Sidebar === */
    section[data-testid="stSidebar"] .stRadio label {
        font-weight: 600;
        color: white;
    }

    /* === Styling tiap pilihan menu === */
    .stRadio > div {
        gap: 0.5rem;
    }

    /* === Warna pilihan menu (tidak aktif) === */
    .stRadio div[role="radiogroup"] > label {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        transition: 0.2s ease;
        margin-bottom: 0.3rem;
    }

    /* === Warna pilihan menu (hover) === */
    .stRadio div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.25);
        cursor: pointer;
    }

    /* === Warna pilihan menu (aktif/selected) === */
    .stRadio div[role="radiogroup"] > label[data-selected="true"] {
        background-color: rgba(255, 255, 255, 0.4);
        color: #2c3e50;
        font-weight: bold;
    }

    
    /* Results section */
    .results-header {
        background: linear-gradient(135deg, #813772 0%, #B82601 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 600;
        text-align: center;
    }
    
    /* Animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Highlight text */
    .highlight-keyword {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-weight: bold;
    }
    
    /* Warning and success messages */
    .stAlert > div {
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
    }
    
    /* Footer styling */
    .footer-section {
        background: rgba(255,255,255,0.95);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
        /* Perbesar isi st.dataframe */
    iframe[data-testid="stDataFrame"] {
        min-height: 450px !important;
        height: auto !important;
        zoom: 1.2;
    }

    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# Konfigurasi halaman
st.set_page_config(
    page_title="Mesin Pencarian Naskah Carita Parahyangan", 
    layout="wide",
    page_icon="📜",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# Konfigurasi Apache Jena Fuseki
FUSEKI_ENDPOINT = "http://localhost:3030/CaritaParahyangan/sparql"
FUSEKI_UPDATE_ENDPOINT = "http://localhost:3030/NaskahParahyangan/update"

# Fungsi untuk query dengan SPARQL endpoint
def query_with_fuseki(sparql_query):
    try:
        sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        st.error(f"Error connecting to Fuseki: {str(e)}")
        return []

# Fungsi untuk test koneksi ke Fuseki
def test_fuseki_connection():
    try:
        response = requests.get(f"http://localhost:3030/$/ping", timeout=5)
        return response.status_code == 200
    except:
        return False

# Fungsi pencarian berdasarkan kata kunci
def search_by_keyword(keyword, search_type="all"):
    """
    search_type: 'all', 'aksara', 'transliterasi', 'terjemahan'
    """
    base_query = """
    PREFIX : <http://contoh.org/ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT DISTINCT ?baris ?aksara ?transliterasi ?terjemahan
    WHERE {
        ?baris a :BarisNaskah ;
            :mengandungAksara ?aksaraObj ;
            :hasTransliteration ?translitObj ;
            :hasTranslation ?terjemahObj .
        ?aksaraObj rdf:value ?aksara .
        ?translitObj rdf:value ?transliterasi .
        ?terjemahObj rdf:value ?terjemahan .
    """
    
    # Tambahkan filter berdasarkan jenis pencarian
    if search_type == "aksara":
        filter_clause = f'FILTER(CONTAINS(LCASE(?aksara), LCASE("{keyword}")))'
    elif search_type == "transliterasi":
        filter_clause = f'FILTER(CONTAINS(LCASE(?transliterasi), LCASE("{keyword}")))'
    elif search_type == "terjemahan":
        filter_clause = f'FILTER(CONTAINS(LCASE(?terjemahan), LCASE("{keyword}")))'
    else:  # search all
        filter_clause = f"""FILTER(
            CONTAINS(LCASE(?aksara), LCASE("{keyword}")) ||
            CONTAINS(LCASE(?transliterasi), LCASE("{keyword}")) ||
            CONTAINS(LCASE(?terjemahan), LCASE("{keyword}"))
        )"""
    
    query = base_query + "\n" + filter_clause + "\n} ORDER BY ?baris LIMIT 50"
    return query

# Fungsi untuk highlight kata kunci
def highlight_text(text, keyword):
    if not keyword or not text:
        return text
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(f'<span class="highlight-keyword">{keyword.upper()}</span>', str(text))

# Fungsi untuk mengextract value dari binding SPARQL
def extract_value(binding, key):
    if key in binding:
        return binding[key]["value"]
    return ""

# Custom header
st.markdown("""
<div class="main-header fade-in">
    <h1>📜 Mesin Pencarian Naskah Carita Parahyangan</h1>
    <p>Portal Web Semantik untuk Mengeksplorasi Naskah Sunda Kuno dalam Aksara Cacarakan</p>
</div>
""", unsafe_allow_html=True)

# Status koneksi di sidebar dengan styling
st.sidebar.markdown("""
<div class="sidebar-content">
    <h2 style="color: white; text-align: center; margin-bottom: 0.5rem; margin-top: 0.5rem;">🔍 Menu Navigasi</h2>
</div>
""", unsafe_allow_html=True)


# Test koneksi
connection_status = test_fuseki_connection()

if connection_status:
    st.sidebar.markdown("""
    <div class="status-connected">
        🟢 Terhubung ke Apache Jena Fuseki
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div class="status-disconnected">
        🔴 Tidak dapat terhubung ke Apache Jena Fuseki
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.info("💡 Pastikan Fuseki berjalan di http://localhost:3030")

# Ambil query params
params = st.query_params
current_page = params.get("page", "beranda")

# Daftar menu navigasi
menu_options = {
    "🏠 Beranda": "beranda",
    "🔍 Pencarian Umum": "pencarian-umum",
    "🔬 Pencarian Lanjutan": "pencarian-lanjutan",
    "📚 Jelajah Data": "jelajah",
    "📊 Statistik": "statistik",
    "⚙️ Pengaturan": "pengaturan"
}

# Buat lookup kebalikannya
menu_lookup = {v: k for k, v in menu_options.items()}

# Inisialisasi default menu dari query param
default_menu_key = menu_lookup.get(current_page, "🏠 Beranda")  # ← sekarang sudah aman

# Sidebar menu
selected_menu = st.sidebar.radio(
    "Pilih Menu:",
    options=list(menu_options.keys()),
    index=list(menu_options.keys()).index(default_menu_key)
)

# Halaman aktif
menu = menu_options[selected_menu]



if menu == "beranda":
    # st.markdown("""
    # <div class="info-card fade-in">
    #     <h2 style="color: #2c3e50; text-align: center; margin-bottom: 1.5rem;">
    #         🌟 Selamat Datang di Portal Naskah Cacarakan
    #     </h2>
    #     <p style="font-size: 1.1rem; text-align: center; color: #7f8c8d; margin-bottom: 2rem;">
    #         Portal pencarian berbasis web semantik untuk mengeksplorasi naskah Sunda kuno Carita Parahyangan 
    #         dalam Aksara Cacarakan menggunakan Apache Jena Fuseki sebagai triplestore.
    #     </p>
    # </div>
    # """, unsafe_allow_html=True)

    # Baris 1
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""<div class="feature-card fade-in">""", unsafe_allow_html=True)
        st.markdown("### 🔍 Pencarian Umum")
        st.markdown("Cari berdasarkan kata kunci dalam aksara, transliterasi, atau terjemahan dengan algoritma pencarian canggih")
        if st.button("➡️ Masuk", key="btn_umum"):
            st.query_params.update({"page": "pencarian-umum"})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="feature-card fade-in">""", unsafe_allow_html=True)
        st.markdown("### 🔬 Pencarian Lanjutan")
        st.markdown("Filter hasil berdasarkan kriteria spesifik dengan kontrol pencarian yang detail")
        if st.button("➡️ Masuk", key="btn_lanjutan"):
            st.query_params.update({"page": "pencarian-lanjutan"})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Baris 2
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""<div class="feature-card fade-in">""", unsafe_allow_html=True)
        st.markdown("### 📚 Jelajah Data")
        st.markdown("Telusuri seluruh koleksi naskah dengan navigasi yang mudah dan intuitif")
        if st.button("➡️ Masuk", key="btn_jelajah"):
            st.query_params.update({"page": "jelajah"})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("""<div class="feature-card fade-in">""", unsafe_allow_html=True)
        st.markdown("### 📊 Statistik")
        st.markdown("Lihat analisis data naskah dengan visualisasi yang informatif dan menarik")
        if st.button("➡️ Masuk", key="btn_statistik"):
            st.query_params.update({"page": "statistik"})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)



# Halaman Pencarian Umum
elif menu == "pencarian-umum":
    # Header pencarian
    st.markdown("""
    <div class="fade-in" style="
        color: white;
        text-align: center;
        margin: 1rem 0 2rem 0;
    ">
        <h2 style="color: white; margin-bottom: 0.8rem;">
            🔍 Pencarian Kata Kunci
        </h2>
        <p style="font-size: 0.95rem; color: #dfe6e9; margin: 0;">
            Cari istilah dalam aksara Cacarakan, transliterasi, atau terjemahan secara semantik.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Cek koneksi ke Fuseki
    if not connection_status:
        st.error("⚠️ Tidak dapat terhubung ke server Apache Jena Fuseki. Periksa koneksi dan pastikan server berjalan.")
        st.stop()

    # Input kata kunci & filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Masukkan kata kunci:",
            placeholder="Contoh: raja, kerajaan, atau kata dalam aksara Cacarakan",
            help="Masukkan kata kunci yang ingin Anda cari dalam naskah"
        )

    with col2:
        search_type = st.selectbox(
            "Cari dalam:",
            ["Semua", "Aksara Cacarakan", "Transliterasi", "Terjemahan"],
            index=0,
            help="Pilih jenis teks yang ingin dicari"
        )

    # Tombol pencarian di kanan
    btn_col1, btn_col2, btn_col3 = st.columns([5, 1, 1])
    with btn_col3:
        start_search = st.button("🚀 Mulai Pencarian", type="primary")

    # Mapping jenis pencarian
    type_mapping = {
        "Semua": "all",
        "Aksara Cacarakan": "aksara",
        "Transliterasi": "transliterasi",
        "Terjemahan": "terjemahan"
    }

    # Eksekusi pencarian jika tombol ditekan
    if start_search:
        if search_query:
            with st.spinner("🔄 Mencari data di Apache Jena Fuseki..."):
                query = search_by_keyword(search_query, type_mapping[search_type])
                results = query_with_fuseki(query)

                if results:
                    st.markdown(f"### ✅ Ditemukan hasil pencarian untuk: `{search_query}`")

                    # Fungsi untuk highlight kata yang dicari
                    def highlight_text(text, search_term):
                        if not text or not search_term:
                            return text
                        # Case-insensitive highlighting
                        import re
                        pattern = re.compile(re.escape(search_term), re.IGNORECASE)
                        return pattern.sub(f'<mark style="background-color: #ffeb3b; color: #000; padding: 2px 4px; border-radius: 3px;">{search_term}</mark>', text)

                    result_data = []
                    for row in results:
                        aksara = extract_value(row, "aksara")
                        transliterasi = extract_value(row, "transliterasi")
                        terjemahan = extract_value(row, "terjemahan")

                        # Highlight kata yang dicari berdasarkan jenis pencarian
                        if search_type == "Semua":
                            aksara_highlighted = highlight_text(aksara, search_query)
                            transliterasi_highlighted = highlight_text(transliterasi, search_query)
                            terjemahan_highlighted = highlight_text(terjemahan, search_query)
                        elif search_type == "Aksara Cacarakan":
                            aksara_highlighted = highlight_text(aksara, search_query)
                            transliterasi_highlighted = transliterasi
                            terjemahan_highlighted = terjemahan
                        elif search_type == "Transliterasi":
                            aksara_highlighted = aksara
                            transliterasi_highlighted = highlight_text(transliterasi, search_query)
                            terjemahan_highlighted = terjemahan
                        elif search_type == "Terjemahan":
                            aksara_highlighted = aksara
                            transliterasi_highlighted = transliterasi
                            terjemahan_highlighted = highlight_text(terjemahan, search_query)

                        result_data.append({
                            "Aksara Cacarakan": aksara_highlighted,
                            "Transliterasi": transliterasi_highlighted,
                            "Terjemahan": terjemahan_highlighted
                        })

                    # Buat DataFrame dengan index mulai dari 1
                    df = pd.DataFrame(result_data)
                    df.index = df.index + 1
                    
                    # Tampilkan dengan st.markdown untuk mendukung HTML
                    st.markdown("---")
                    
                    # Convert DataFrame to HTML table with highlighting
                    html_table = df.to_html(escape=False, classes='highlight-table')
                    
                    # Custom CSS untuk styling tabel
                    st.markdown("""
                    <style>
                    .highlight-table {
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                        font-size: 14px;
                        background-color: #1e1e1e;
                        color: white;
                    }
                    .highlight-table th, .highlight-table td {
                        border: 1px solid #444;
                        padding: 12px;
                        text-align: left;
                        vertical-align: top;
                    }
                    .highlight-table th {
                        background-color: #333;
                        font-weight: bold;
                        color: #fff;
                    }
                    .highlight-table tr:nth-child(even) {
                        background-color: #2a2a2a;
                    }
                    .highlight-table tr:nth-child(odd) {
                        background-color: #1e1e1e;
                    }
                    .highlight-table tr:hover {
                        background-color: #3a3a3a;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Tampilkan tabel dengan HTML
                    st.markdown(html_table, unsafe_allow_html=True)
                    st.info(f"📊 Menampilkan {len(result_data)} hasil dari pencarian '{search_query}'")
                else:
                    st.warning(f"❌ Tidak ditemukan hasil untuk kata kunci: **{search_query}**")
                    st.info("💡 Coba gunakan kata kunci yang berbeda atau periksa ejaan.")
        else:
            st.warning("⚠️ Silakan masukkan kata kunci pencarian terlebih dahulu")

# Halaman Pencarian Lanjutan
elif menu == "pencarian-lanjutan":
    st.markdown("""
    <div class="fade-in" style="
        color: white;
        text-align: center;
        margin: 2rem 0 2rem 0;
    ">
        <h2 style="color: white; margin-bottom: 0.8rem;">
            🔬 Pencarian Lanjutan
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    if not connection_status:
        st.error("⚠️ Tidak dapat terhubung ke server Apache Jena Fuseki.")
        st.stop()
    
    st.markdown("""
    <div class="fade-in">
        <h3 style="color: #ffffff;">🎛️ Filter Berdasarkan Kriteria</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_length = st.number_input("📏 Panjang minimum transliterasi:", min_value=0, value=0)
        search_keyword = st.text_input("🔍 Kata kunci:", placeholder="Masukkan kata kunci opsional")
    
    with col2:
        max_length = st.number_input("📏 Panjang maksimum transliterasi:", min_value=0, value=1000)
        sort_by = st.selectbox("📋 Urutkan berdasarkan:", ["Baris", "Panjang Teks", "Alfabetis"])

    # Tombol pencarian di kanan dan lebar otomatis
    btn_left, btn_spacer, btn_right = st.columns([4, 1, 1])
    with btn_right:
        start_filter_search = st.button("🚀 Cari dengan Filter", type="primary")

    if start_filter_search:
        with st.spinner("🔄 Memproses pencarian lanjutan di Fuseki..."):
            query = f"""
            PREFIX : <http://contoh.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            
            SELECT ?baris ?aksara ?transliterasi ?terjemahan
            WHERE {{
                ?baris a :BarisNaskah ;
                    :mengandungAksara ?aksaraObj ;
                    :hasTransliteration ?translitObj ;
                    :hasTranslation ?terjemahObj .
                ?aksaraObj rdf:value ?aksara .
                ?translitObj rdf:value ?transliterasi .
                ?terjemahObj rdf:value ?terjemahan .
                FILTER(STRLEN(?transliterasi) >= {min_length} && STRLEN(?transliterasi) <= {max_length})
            """

            if search_keyword:
                query += f"""
                FILTER(
                    CONTAINS(LCASE(?aksara), LCASE("{search_keyword}")) ||
                    CONTAINS(LCASE(?transliterasi), LCASE("{search_keyword}")) ||
                    CONTAINS(LCASE(?terjemahan), LCASE("{search_keyword}"))
                )
                """
            query += "} ORDER BY ?baris LIMIT 100"

            results = query_with_fuseki(query)
            
            if results:
                result_data = []
                for row in results:
                    aksara = extract_value(row, "aksara")
                    transliterasi = extract_value(row, "transliterasi")
                    terjemahan = extract_value(row, "terjemahan")
                    result_data.append({
                        "Aksara Cacarakan": aksara,
                        "Transliterasi": transliterasi,
                        "Terjemahan": terjemahan,
                        "Panjang": len(transliterasi)
                    })

                # Buat DataFrame dengan index mulai dari 1
                df = pd.DataFrame(result_data)
                df.index = df.index + 1

                # Sorting
                if sort_by == "Panjang Teks":
                    df = df.sort_values("Panjang", ascending=False)
                    # Reset index setelah sorting agar tetap berurutan 1, 2, 3...
                    df.index = range(1, len(df) + 1)
                elif sort_by == "Alfabetis":
                    df = df.sort_values("Transliterasi")
                    # Reset index setelah sorting agar tetap berurutan 1, 2, 3...
                    df.index = range(1, len(df) + 1)

                # Tampilkan dengan st.table()
                st.table(df)
                st.success(f"✅ Ditemukan {len(result_data)} hasil sesuai kriteria")
            else:
                st.warning("❌ Tidak ada hasil yang sesuai dengan kriteria pencarian")


# Halaman Jelajah Data
elif menu == "jelajah":
    # st.markdown("""
    # <div class="search-section fade-in">
    #     <h2 style="color: #2c3e50; text-align: center; margin-bottom: 1.5rem;">
    #         📚 Jelajah Data Naskah
    #     </h2>
    # </div>
    # """, unsafe_allow_html=True)
    
    # Inisialisasi session_state untuk halaman jika belum ada
    # Inisialisasi session state
    if "page_number" not in st.session_state:
        st.session_state.page_number = 1

    if not connection_status:
        st.error("⚠️ Tidak dapat terhubung ke server Apache Jena Fuseki.")
        st.stop()

    st.markdown("""
    <div class="fade-in">
        <h3 style="color: #ffffff;">📖 Semua Data Naskah</h3>
    </div>
    """, unsafe_allow_html=True)

    # Pilihan jumlah data per halaman
    page_size_option = st.selectbox(
        "📄 Jumlah data per halaman:",
        [10, 25, 50, 100, "All"],
        index=1,
        help="Pilih jumlah data yang ditampilkan per halaman"
    )

    # Hitung total data
    count_query = """
    PREFIX : <http://contoh.org/ontology#>
    SELECT (COUNT(?baris) as ?total)
    WHERE {
        ?baris a :BarisNaskah .
    }
    """
    count_results = query_with_fuseki(count_query)
    total_data = int(extract_value(count_results[0], "total")) if count_results else 0

    if total_data > 0:
        if page_size_option == "All":
            page_size = total_data
            offset = 0
            st.session_state.page_number = 1
            max_pages = 1
        else:
            page_size = int(page_size_option)
            max_pages = (total_data + page_size - 1) // page_size
            page_number = st.session_state.page_number
            page_number = max(1, min(page_number, max_pages))
            st.session_state.page_number = page_number
            offset = (page_number - 1) * page_size

        # Query data dengan LIMIT dan OFFSET
        browse_query = f"""
        PREFIX : <http://contoh.org/ontology#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?baris ?aksara ?transliterasi ?terjemahan
        WHERE {{
            ?baris a :BarisNaskah ;
                :mengandungAksara ?aksaraObj ;
                :hasTransliteration ?translitObj ;
                :hasTranslation ?terjemahObj .
            ?aksaraObj rdf:value ?aksara .
            ?translitObj rdf:value ?transliterasi .
            ?terjemahObj rdf:value ?terjemahan .
        }}
        ORDER BY ?baris
        LIMIT {page_size}
        OFFSET {offset}
        """
        results = query_with_fuseki(browse_query)

        if results:
            result_data = []
            for row in results:  # Removed the enumerate with counter
                result_data.append({
                    "Aksara Cacarakan": extract_value(row, "aksara"),
                    "Transliterasi": extract_value(row, "transliterasi"),
                    "Terjemahan": extract_value(row, "terjemahan")
                })

            # Buat DataFrame dengan index mulai dari nomor sesuai pagination
            df = pd.DataFrame(result_data)
            df.index = range(offset + 1, offset + len(df) + 1)

            # Tampilkan DataFrame tanpa scroll kosong
            st.table(df)

            # Info halaman
            if page_size_option == "All":
                st.info(f"📄 Menampilkan semua {total_data} data")
            else:
                start_idx = offset + 1
                end_idx = min(offset + page_size, total_data)
                st.info(f"📄 Menampilkan data {start_idx}–{end_idx} dari {total_data} total data | Halaman {page_number} dari {max_pages}")

                # Tombol navigasi
                col1, col2 = st.columns([7, 1])
                with col1:
                    if st.session_state.page_number > 1:
                        if st.button("⬅️ Sebelumnya"):
                            st.session_state.page_number -= 1
                            st.experimental_rerun()
                with col2:
                    if st.session_state.page_number < max_pages:
                        if st.button("➡️ Selanjutnya"):
                            st.session_state.page_number += 1
                            st.experimental_rerun()
        else:
            st.warning("❌ Tidak ada data ditemukan.")
    else:
        st.warning("📭 Tidak ada data dalam basis data.")
    
# Halaman Statistik
elif menu == "statistik":
    st.markdown("""
    <div class="search-section fade-in">
        <h2 style="color: #ffffff; text-align: center; margin-bottom: 1.5rem;">
            📊 Statistik Data Naskah
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    if not connection_status:
        st.error("⚠️ Tidak dapat terhubung ke server Apache Jena Fuseki.")
        st.stop()
    
    # Query untuk statistik dasar
    stats_query = """
    PREFIX : <http://contoh.org/ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT 
        (COUNT(?baris) as ?totalBaris)
        (AVG(STRLEN(?transliterasi)) as ?avgLength)
        (MIN(STRLEN(?transliterasi)) as ?minLength)
        (MAX(STRLEN(?transliterasi)) as ?maxLength)
    WHERE {
        ?baris a :BarisNaskah ;
            :hasTransliteration ?translitObj .
        ?translitObj rdf:value ?transliterasi .
    }
    """
    
    stats_results = query_with_fuseki(stats_query)
    
    if stats_results:
        row = stats_results[0]
        
        # Custom metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card fade-in">
                <h3>📚</h3>
                <h2>{int(float(extract_value(row, "totalBaris")))}</h2>
                <p>Total Baris</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card fade-in">
                <h3>📏</h3>
                <h2>{float(extract_value(row, 'avgLength')):.1f}</h2>
                <p>Rata-rata Panjang</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card fade-in">
                <h3>📉</h3>
                <h2>{int(float(extract_value(row, "minLength")))}</h2>
                <p>Panjang Minimum</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card fade-in">
                <h3>📈</h3>
                <h2>{int(float(extract_value(row, "maxLength")))}</h2>
                <p>Panjang Maksimum</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Distribusi panjang teks
    st.markdown("""
    <div class="fade-in"
        style=" background: linear-gradient(135deg, #2c3e50, #3498db);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;"
        >
        <h3 style="color: #ffffff; text-align: center;">📊 Distribusi Panjang Transliterasi</h3>
    </div>
    """, unsafe_allow_html=True)
    
    length_query = """
    PREFIX : <http://contoh.org/ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?transliterasi
    WHERE {
        ?baris a :BarisNaskah ;
            :hasTransliteration ?translitObj .
        ?translitObj rdf:value ?transliterasi .
    }
    """
    
    length_results = query_with_fuseki(length_query)
    
    if length_results:
        lengths = [len(extract_value(row, "transliterasi")) for row in length_results]
        
        # Buat histogram sederhana
        length_df = pd.DataFrame({'Panjang': lengths})
        
        # Kategorisasi panjang
        length_df['Kategori'] = pd.cut(length_df['Panjang'], 
                                     bins=[0, 20, 50, 100, 200, float('inf')], 
                                     labels=['Sangat Pendek (0-20)', 'Pendek (21-50)', 
                                            'Sedang (51-100)', 'Panjang (101-200)', 
                                            'Sangat Panjang (>200)'])
        
        category_counts = length_df['Kategori'].value_counts()
        
        st.bar_chart(category_counts)
        
        # Tabel distribusi
        st.markdown("""
        <div class="fade-in"
        style=" background: linear-gradient(135deg, #2c3e50, #3498db);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;"
        >
            <h3 style="color: #ffffff; text-align: center;">📋 Detail Distribusi</h3>
        </div>
        """, unsafe_allow_html=True)
        
        dist_df = pd.DataFrame({
            'Kategori Panjang': category_counts.index,
            'Jumlah': category_counts.values,
            'Persentase': (category_counts.values / len(lengths) * 100).round(2)
        })
        st.table(dist_df)

# Halaman Pengaturan
elif menu == "pengaturan":
    st.markdown("""
    <div class="fade-in">
        <h2 style="color: #ffffff; text-align: center; margin-bottom: 1.5rem;">
            ⚙️ Pengaturan Koneksi
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="">
        <h3 style="color: #ffffff;">🔧 Konfigurasi Apache Jena Fuseki</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_endpoint = st.text_input("🌐 SPARQL Endpoint:", value=FUSEKI_ENDPOINT, help="URL endpoint untuk query SPARQL")
        
    with col2:
        current_update_endpoint = st.text_input("🔄 Update Endpoint:", value=FUSEKI_UPDATE_ENDPOINT, help="URL endpoint untuk update data")
    
    if st.button("🔗 Test Koneksi", type="primary"):
        with st.spinner("🔄 Testing koneksi..."):
            try:
                response = requests.get("http://localhost:3030/$/ping", timeout=5)
                if response.status_code == 200:
                    st.success("✅ Koneksi ke Apache Jena Fuseki berhasil!")
                    
                    # Test query sederhana
                    test_query = """
                    PREFIX : <http://contoh.org/ontology#>
                    SELECT (COUNT(?s) as ?count) WHERE { ?s ?p ?o }
                    """
                    results = query_with_fuseki(test_query)
                    if results:
                        total_triples = extract_value(results[0], "count")
                        st.info(f"📊 Total triples dalam dataset: {total_triples}")
                else:
                    st.error("❌ Server Fuseki tidak merespons dengan benar")
            except Exception as e:
                st.error(f"❌ Gagal terhubung ke Fuseki: {str(e)}")
    
    st.markdown("""
    <div class="fade-in"
        style=" background: linear-gradient(135deg, #2c3e50, #3498db);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;"
        >
        <h3 style="color: #ffffff;">📊 Informasi Dataset</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if connection_status:
        # Query untuk informasi dataset
        dataset_info_query = """
        PREFIX : <http://contoh.org/ontology#>
        SELECT 
            (COUNT(DISTINCT ?s) as ?subjects)
            (COUNT(DISTINCT ?p) as ?predicates)
            (COUNT(DISTINCT ?o) as ?objects)
            (COUNT(*) as ?triples)
        WHERE { ?s ?p ?o }
        """
        
        dataset_results = query_with_fuseki(dataset_info_query)
        if dataset_results:
            row = dataset_results[0]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎯</h3>
                    <h2>{extract_value(row, "subjects")}</h2>
                    <p>Subjects</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🔗</h3>
                    <h2>{extract_value(row, "predicates")}</h2>
                    <p>Predicates</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📦</h3>
                    <h2>{extract_value(row, "objects")}</h2>
                    <p>Objects</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🔢</h3>
                    <h2>{extract_value(row, "triples")}</h2>
                    <p>Total Triples</p>
                </div>
                """, unsafe_allow_html=True)

# Footer dengan styling menarik
st.markdown("""
<div class="footer-section fade-in" style="
    background: linear-gradient(180deg, #34495e, #2c3e50);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin-top: 2rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
">
    <h3 style="margin-bottom: 0.8rem;">
        🏛️ Portal Web Semantik Naskah Sunda Kuno
    </h3>
    <p style="font-size: 0.95rem; margin-bottom: 1rem;">
        Menggunakan Apache Jena Fuseki sebagai triplestore dan SPARQL untuk query semantik
    </p>
    <div style="margin-top: 1rem;">
        <span style="
            background: rgba(255,255,255,0.15);
            color: white; 
            padding: 0.4rem 0.9rem; 
            border-radius: 20px; 
            margin: 0.2rem;
            display: inline-block;
            font-size: 0.9rem;
        ">
            🔍 Web Semantik
        </span>
        <span style="
            background: rgba(255,255,255,0.15);
            color: white; 
            padding: 0.4rem 0.9rem; 
            border-radius: 20px; 
            margin: 0.2rem;
            display: inline-block;
            font-size: 0.9rem;
        ">
            📜 Naskah Kuno
        </span>
        <span style="
            background: rgba(255,255,255,0.15);
            color: white; 
            padding: 0.4rem 0.9rem; 
            border-radius: 20px; 
            margin: 0.2rem;
            display: inline-block;
            font-size: 0.9rem;
        ">
            🌐 Apache Jena
        </span>
        <span style="
            background: rgba(255,255,255,0.15);
            color: white; 
            padding: 0.4rem 0.9rem; 
            border-radius: 20px; 
            margin: 0.2rem;
            display: inline-block;
            font-size: 0.9rem;
        ">
            💾 SPARQL
        </span>
    </div>
</div>
""", unsafe_allow_html=True)