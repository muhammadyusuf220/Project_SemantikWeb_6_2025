import streamlit as st
from rdflib import Graph
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Cacarakan Semantic Web", layout="wide")

# Fungsi untuk query dengan RDFlib
def query_with_rdflib(query, data_file):
    g = Graph()
    g.parse(data_file, format='turtle')
    results = g.query(query)
    return results

# Sidebar navigasi
st.sidebar.title("Navigasi")
menu = st.sidebar.radio(
    "Pilih Menu",
    ["Beranda", "Transliterasi", "Translasi"]
)

# Halaman Beranda
if menu == "Beranda":
    st.title("Portal Web Semantik Naskah Cacarakan")
    st.markdown("""
    ### Tentang Aplikasi
    Aplikasi ini memanfaatkan teknologi web semantik untuk mengeksplorasi dan menganalisis naskah Sunda kuno 
    yang menggunakan Aksara Cacarakan.
    """)
    
    st.markdown("""
    ### Fitur Utama:
    - Transliterasi: Konversi Aksara ke Latin
    - Translasi: Terjemahan teks Latin ke Bahasa Indonesia
    """)

# Halaman Transliterasi
elif menu == "Transliterasi":
    st.title("Transliterasi Cacarakan ke Latin")
    
    # Load data
    g = Graph()
    g.parse("data/cacarakan.ttl", format="turtle")
    
    # Input teks Cacarakan
    input_text = st.text_area("Masukkan teks dalam Aksara Cacarakan", height=100)
    
    if st.button("Transliterasikan"):
        if input_text:
            # Query untuk transliterasi
            query = """
            PREFIX : <http://contoh.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            
            SELECT ?transliterasi
            WHERE {
                ?baris a :BarisNaskah ;
                    :mengandungAksara ?aksara ;
                    :hasTransliteration ?translit .
                ?aksara rdf:value ?aksaraValue .
                ?translit rdf:value ?transliterasi .
                FILTER(STRSTARTS(?aksaraValue, "%s"))
            }
            """ % input_text[:20]  # Ambil sebagian teks untuk pencarian
            
            results = g.query(query)
            
            if results:
                st.subheader("Hasil Transliterasi")
                for row in results:
                    st.write(row.transliterasi)
            else:
                st.warning("Teks tidak ditemukan dalam basis data")
        else:
            st.warning("Silakan masukkan teks terlebih dahulu")
    
    # Tampilkan contoh transliterasi
    st.subheader("Contoh Transliterasi")
    query_examples = """
    PREFIX : <http://contoh.org/ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?aksara ?transliterasi
    WHERE {
        ?baris a :BarisNaskah ;
            :mengandungAksara ?aksaraObj ;
            :hasTransliteration ?translitObj .
        ?aksaraObj rdf:value ?aksara ;
                  :jumlahKarakter ?jml .
        ?translitObj rdf:value ?transliterasi .
    }
    ORDER BY ?baris
    LIMIT 5
    """
    
    examples = query_with_rdflib(query_examples, "data/cacarakan.ttl")
    example_data = []
    for row in examples:
        example_data.append({
            "Aksara Cacarakan": row.aksara,
            "Transliterasi Latin": row.transliterasi
        })
    
    df = pd.DataFrame(example_data)
    st.table(df)

# Halaman Translasi
elif menu == "Translasi":
    st.title("Translasi Latin ke Bahasa Indonesia")
    
    # Load data
    g = Graph()
    g.parse("data/cacarakan.ttl", format="turtle")
    
    # Input teks Latin
    input_text = st.text_area("Masukkan teks dalam Latin", height=100)
    
    if st.button("Terjemahkan"):
        if input_text:
            # Query untuk translasi
            query = """
            PREFIX : <http://contoh.org/ontology#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            
            SELECT ?terjemahan
            WHERE {
                ?baris a :BarisNaskah ;
                    :hasTransliteration ?translit ;
                    :hasTranslation ?terjemah .
                ?translit rdf:value ?transliterasi .
                ?terjemah rdf:value ?terjemahan .
                FILTER(STRSTARTS(?transliterasi, "%s"))
            }
            """ % input_text[:20]  # Ambil sebagian teks untuk pencarian
            
            results = g.query(query)
            
            if results:
                st.subheader("Hasil Terjemahan")
                for row in results:
                    st.write(row.terjemahan)
            else:
                st.warning("Teks tidak ditemukan dalam basis data")
        else:
            st.warning("Silakan masukkan teks terlebih dahulu")
    
    # Tampilkan contoh terjemahan
    st.subheader("Contoh Translasi")
    query_examples = """
    PREFIX : <http://contoh.org/ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?transliterasi ?terjemahan
    WHERE {
        ?baris a :BarisNaskah ;
            :hasTransliteration ?translit ;
            :hasTranslation ?terjemah .
        ?translit rdf:value ?transliterasi .
        ?terjemah rdf:value ?terjemahan .
    }
    ORDER BY ?baris
    LIMIT 5
    """
    
    examples = query_with_rdflib(query_examples, "data/cacarakan.ttl")
    example_data = []
    for row in examples:
        example_data.append({
            "Teks Latin": row.transliterasi,
            "Terjemahan Indonesia": row.terjemahan
        })
    
    df = pd.DataFrame(example_data)
    st.table(df)

if __name__ == "__main__":
    st.write()