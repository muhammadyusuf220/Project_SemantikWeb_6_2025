import streamlit as st
from rdflib import Graph
import pandas as pd
import re

# Konfigurasi halaman
st.set_page_config(page_title="Mesin Pencarian Naskah Cacarakan", layout="wide")

# Fungsi untuk query dengan RDFlib
def query_with_rdflib(query, data_file):
    try:
        g = Graph()
        g.parse(data_file, format='turtle')
        results = g.query(query)
        return results
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return []

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

# Sidebar navigasi
st.sidebar.title("🔍 Menu Pencarian")
menu = st.sidebar.radio(
    "Pilih Jenis Pencarian",
    ["Pencarian Umum", "Pencarian Lanjutan", "Jelajah Data", "Statistik"]
)

# Header aplikasi
st.title("🔍 Mesin Pencarian Naskah Cacarakan")
st.markdown("""
Portal pencarian berbasis web semantik untuk mengeksplorasi naskah Sunda kuno dalam Aksara Cacarakan.
""")

# Halaman Pencarian Umum
if menu == "Pencarian Umum":
    st.header("Pencarian Kata Kunci")
    
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
            with st.spinner("Mencari data..."):
                query = search_by_keyword(search_query, type_mapping[search_type])
                results = query_with_rdflib(query, "data/output.ttl")
                
                if results:
                    st.success(f"Ditemukan hasil pencarian untuk: **{search_query}**")
                    
                    # Tampilkan hasil dalam tabel
                    result_data = []
                    for i, row in enumerate(results, 1):
                        result_data.append({
                            "No": i,
                            "Aksara Cacarakan": highlight_text(row.aksara, search_query if search_type in ["Semua", "Aksara Cacarakan"] else ""),
                            "Transliterasi": highlight_text(row.transliterasi, search_query if search_type in ["Semua", "Transliterasi"] else ""),
                            "Terjemahan": highlight_text(row.terjemahan, search_query if search_type in ["Semua", "Terjemahan"] else "")
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
        with st.spinner("Memproses pencarian lanjutan..."):
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
            
            results = query_with_rdflib(query, "data/output.ttl")
            
            if results:
                result_data = []
                for i, row in enumerate(results, 1):
                    result_data.append({
                        "No": i,
                        "Aksara Cacarakan": str(row.aksara),
                        "Transliterasi": str(row.transliterasi),
                        "Terjemahan": str(row.terjemahan),
                        "Panjang": len(str(row.transliterasi))
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
    
    count_results = query_with_rdflib(count_query, "data/output.ttl")
    total_data = 0
    for row in count_results:
        total_data = int(row.total)
    
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
        
        results = query_with_rdflib(browse_query, "data/output.ttl")
        
        if results:
            result_data = []
            for i, row in enumerate(results, offset + 1):
                result_data.append({
                    "No": i,
                    "Aksara Cacarakan": str(row.aksara),
                    "Transliterasi": str(row.transliterasi),
                    "Terjemahan": str(row.terjemahan)
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
    
    stats_results = query_with_rdflib(stats_query, "data/output.ttl")
    
    if stats_results:
        for row in stats_results:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📚 Total Baris", int(row.totalBaris))
            with col2:
                st.metric("📏 Rata-rata Panjang", f"{float(row.avgLength):.1f}")
            with col3:
                st.metric("📉 Panjang Minimum", int(row.minLength))
            with col4:
                st.metric("📈 Panjang Maksimum", int(row.maxLength))
    
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
    
    length_results = query_with_rdflib(length_query, "data/output.ttl")
    
    if length_results:
        lengths = [len(str(row.transliterasi)) for row in length_results]
        
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

# Footer
st.markdown("---")
st.markdown("🏛️ **Portal Web Semantik Naskah Cacarakan** - Menggunakan teknologi RDF dan SPARQL untuk eksplorasi data naskah kuno.")