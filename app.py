import streamlit as st
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import re
import requests

# Konfigurasi halaman
st.set_page_config(page_title="Mesin Pencarian Naskah Carita Parahyangan", layout="wide")

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
    return pattern.sub(f"**{keyword.upper()}**", str(text))

# Fungsi untuk mengextract value dari binding SPARQL
def extract_value(binding, key):
    if key in binding:
        return binding[key]["value"]
    return ""

# Status koneksi di sidebar
st.sidebar.title("🔍 Menu Pencarian")

# Test koneksi
connection_status = test_fuseki_connection()
if connection_status:
    st.sidebar.success("🟢 Terhubung ke Apache Jena Fuseki")
else:
    st.sidebar.error("🔴 Tidak dapat terhubung ke Apache Jena Fuseki")
    st.sidebar.info("Pastikan Fuseki berjalan di http://localhost:3030")

menu = st.sidebar.radio(
    "Pilih Jenis Pencarian",
    ["Beranda", "Pencarian Umum", "Pencarian Lanjutan", "Jelajah Data", "Statistik", "Pengaturan"]
)

# Header aplikasi
st.title("🔍 Mesin Pencarian Naskah Carita Parahyangan")

# Halaman Beranda
if menu == "Beranda":
    st.markdown("""
    ## Selamat Datang di Portal Naskah Cacarakan
    
    Portal pencarian berbasis web semantik untuk mengeksplorasi naskah Sunda kuno Carita Parahyangan dalam Aksara Cacarakan.
    Menggunakan Apache Jena Fuseki sebagai triplestore.
    """)
    
    st.markdown("""
    ### Fitur Utama:
    - **Pencarian Umum**: Cari berdasarkan kata kunci dalam aksara, transliterasi, atau terjemahan
    - **Pencarian Lanjutan**: Filter hasil berdasarkan kriteria tertentu
    - **Jelajah Data**: Telusuri seluruh koleksi naskah
    - **Statistik**: Lihat analisis data naskah
    """)


# Halaman Pencarian Umum
elif menu == "Pencarian Umum":
    st.header("Pencarian Kata Kunci")
    
    if not connection_status:
        st.error("⚠️ Tidak dapat terhubung ke server Apache Jena Fuseki. Periksa koneksi dan pastikan server berjalan.")
        st.stop()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Masukkan kata kunci pencarian:",
            placeholder="Contoh: raja, kerajaan, atau kata dalam aksara cacarakan"
        )
    
    with col2:
        search_type = st.selectbox(
            "Cari dalam:",
            ["Semua", "Aksara Cacarakan", "Transliterasi", "Terjemahan"],
            index=0
        )
    
    # Mapping untuk search type
    type_mapping = {
        "Semua": "all",
        "Aksara Cacarakan": "aksara", 
        "Transliterasi": "transliterasi",
        "Terjemahan": "terjemahan"
    }
    
    if st.button("🔍 Cari", type="primary"):
        if search_query:
            with st.spinner("Mencari data di Apache Jena Fuseki..."):
                query = search_by_keyword(search_query, type_mapping[search_type])
                results = query_with_fuseki(query)
                
                if results:
                    st.success(f"Ditemukan hasil pencarian untuk: **{search_query}**")
                    
                    # Tampilkan hasil dalam tabel
                    result_data = []
                    for i, row in enumerate(results, 1):
                        aksara = extract_value(row, "aksara")
                        transliterasi = extract_value(row, "transliterasi")
                        terjemahan = extract_value(row, "terjemahan")
                        
                        result_data.append({
                            "No": i,
                            "Aksara Cacarakan": highlight_text(aksara, search_query if search_type in ["Semua", "Aksara Cacarakan"] else ""),
                            "Transliterasi": highlight_text(transliterasi, search_query if search_type in ["Semua", "Transliterasi"] else ""),
                            "Terjemahan": highlight_text(terjemahan, search_query if search_type in ["Semua", "Terjemahan"] else "")
                        })
                    
                    df = pd.DataFrame(result_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Informasi hasil
                    st.info(f"📊 Menampilkan {len(result_data)} hasil dari pencarian '{search_query}'")
                    
                else:
                    st.warning(f"❌ Tidak ditemukan hasil untuk kata kunci: **{search_query}**")
                    st.info("💡 Coba gunakan kata kunci yang berbeda atau periksa ejaan.")
        else:
            st.warning("⚠️ Silakan masukkan kata kunci pencarian terlebih dahulu")

# Halaman Pencarian Lanjutan
elif menu == "Pencarian Lanjutan":
    st.header("Pencarian Lanjutan")
    
    if not connection_status:
        st.error("⚠️ Tidak dapat terhubung ke server Apache Jena Fuseki.")
        st.stop()
    
    # Filter berdasarkan panjang teks
    st.subheader("Filter Berdasarkan Kriteria")
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_length = st.number_input("Panjang minimum transliterasi:", min_value=0, value=0)
        search_keyword = st.text_input("Kata kunci:", placeholder="Masukkan kata kunci opsional")
    
    with col2:
        max_length = st.number_input("Panjang maksimum transliterasi:", min_value=0, value=1000)
        sort_by = st.selectbox("Urutkan berdasarkan:", ["Baris", "Panjang Teks", "Alfabetis"])
    
    if st.button("🔍 Cari dengan Filter", type="primary"):
        with st.spinner("Memproses pencarian lanjutan di Fuseki..."):
            # Query dengan filter panjang
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
                for i, row in enumerate(results, 1):
                    aksara = extract_value(row, "aksara")
                    transliterasi = extract_value(row, "transliterasi")
                    terjemahan = extract_value(row, "terjemahan")
                    
                    result_data.append({
                        "No": i,
                        "Aksara Cacarakan": aksara,
                        "Transliterasi": transliterasi,
                        "Terjemahan": terjemahan,
                        "Panjang": len(transliterasi)
                    })
                
                df = pd.DataFrame(result_data)
                
                # Sorting
                if sort_by == "Panjang Teks":
                    df = df.sort_values("Panjang", ascending=False)
                elif sort_by == "Alfabetis":
                    df = df.sort_values("Transliterasi")
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.success(f"✅ Ditemukan {len(result_data)} hasil sesuai kriteria")
            else:
                st.warning("❌ Tidak ada hasil yang sesuai dengan kriteria pencarian")

# Halaman Jelajah Data
elif menu == "Jelajah Data":
    st.header("Jelajah Data Naskah")
    
    if not connection_status:
        st.error("⚠️ Tidak dapat terhubung ke server Apache Jena Fuseki.")
        st.stop()
    
    # Tampilkan semua data dengan pagination
    st.subheader("Semua Data Naskah")
    
    # Pagination
    page_size = st.selectbox("Jumlah data per halaman:", [10, 25, 50, 100], index=1)
    
    # Query untuk mendapatkan total data
    count_query = """
    PREFIX : <http://contoh.org/ontology#>
    
    SELECT (COUNT(?baris) as ?total)
    WHERE {
        ?baris a :BarisNaskah .
    }
    """
    
    count_results = query_with_fuseki(count_query)
    total_data = 0
    if count_results:
        total_data = int(extract_value(count_results[0], "total"))
    
    if total_data > 0:
        max_pages = (total_data + page_size - 1) // page_size
        page_number = st.number_input("Halaman:", min_value=1, max_value=max_pages, value=1)
        
        offset = (page_number - 1) * page_size
        
        # Query dengan LIMIT dan OFFSET
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
            for i, row in enumerate(results, offset + 1):
                result_data.append({
                    "No": i,
                    "Aksara Cacarakan": extract_value(row, "aksara"),
                    "Transliterasi": extract_value(row, "transliterasi"),
                    "Terjemahan": extract_value(row, "terjemahan")
                })
            
            df = pd.DataFrame(result_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Info pagination
            start_idx = offset + 1
            end_idx = min(offset + page_size, total_data)
            st.info(f"📄 Menampilkan data {start_idx}-{end_idx} dari {total_data} total data | Halaman {page_number} dari {max_pages}")

# Halaman Statistik
elif menu == "Statistik":
    st.header("Statistik Data Naskah")
    
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
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Total Baris", int(float(extract_value(row, "totalBaris"))))
        with col2:
            st.metric("📏 Rata-rata Panjang", f"{float(extract_value(row, 'avgLength')):.1f}")
        with col3:
            st.metric("📉 Panjang Minimum", int(float(extract_value(row, "minLength"))))
        with col4:
            st.metric("📈 Panjang Maksimum", int(float(extract_value(row, "maxLength"))))
    
    # Distribusi panjang teks
    st.subheader("Distribusi Panjang Transliterasi")
    
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
        st.subheader("Detail Distribusi")
        dist_df = pd.DataFrame({
            'Kategori Panjang': category_counts.index,
            'Jumlah': category_counts.values,
            'Persentase': (category_counts.values / len(lengths) * 100).round(2)
        })
        st.table(dist_df)

# Halaman Pengaturan
elif menu == "Pengaturan":
    st.header("Pengaturan Koneksi")
    
    st.subheader("Konfigurasi Apache Jena Fuseki")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_endpoint = st.text_input("SPARQL Endpoint:", value=FUSEKI_ENDPOINT)
        
    with col2:
        current_update_endpoint = st.text_input("Update Endpoint:", value=FUSEKI_UPDATE_ENDPOINT)
    
    if st.button("🔗 Test Koneksi"):
        with st.spinner("Testing koneksi..."):
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
    
    st.subheader("Informasi Dataset")
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
                st.metric("Subjects", extract_value(row, "subjects"))
            with col2:
                st.metric("Predicates", extract_value(row, "predicates"))
            with col3:
                st.metric("Objects", extract_value(row, "objects"))
            with col4:
                st.metric("Total Triples", extract_value(row, "triples"))

# Footer
st.markdown("---")
st.markdown("🏛️ **Portal Web Semantik Naskah Sunda Kuno** - Menggunakan Apache Jena Fuseki sebagai triplestore dan SPARQL untuk query semantik.")