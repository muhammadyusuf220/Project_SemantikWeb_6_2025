import csv

def generate_turtle_from_csv(csv_file, output_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        data = list(reader)

    with open(output_file, 'w', encoding='utf-8') as out:
        # Prefix RDF
        out.write('''@prefix : <http://contoh.org/ontology#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

### DEKLARASI UTAMA ###
:naskahSunda01 a :Manuskrip ;
    dcterms:title "Carita Parahiyangan"@su ;
    dcterms:alternative "Carita Parahyangan"@su ;
    dcterms:creator "Anonim" ;
    dcterms:language "su" ;
    :ditulisMenggunakan :AksaraCacarakan ;
    :periode "Abad ke-16" ;
    :lokasiPenyimpanan "Naskah koleksi pribadi" .

:AksaraCacarakan a :SistemTulisan ;
    rdfs:label "Aksara Cacarakan"@id ;
    :berasalDariWilayah "Tatar Sunda"@id ;
    :merupakanVarianDari :AksaraSundaKuno .

### BAGIAN I TEKS ###
''')

        for row in data:
            urutan = row['urutan'].strip()
            baris_id = f"baris{urutan.zfill(3)}"
            aksara_id = f"aksara_{baris_id}"
            translit_id = f"translit_{baris_id}"
            terjemah_id = f"terjemah_{baris_id}"
            identifier = row['id'].strip()
            aksara = row['aksara'].strip().replace('"', '\\"')
            transliterasi = row['transliterasi'].strip().replace('"', '\\"')
            terjemahan = row['terjemahan'].strip().replace('"', '\\"')
            jumlah_karakter = len(aksara)

            out.write(f'''
:{baris_id} a :BarisNaskah ;
    :isFromManuscript :naskahSunda01 ;
    :mengandungAksara :{aksara_id} ;
    :hasTransliteration :{translit_id} ;
    :hasTranslation :{terjemah_id} ;
    :urutan "{urutan}"^^xsd:integer ;
    dcterms:identifier "{identifier}" .

:{aksara_id} a :TeksAksara ;
    rdf:value "{aksara}"@su-x-cacarakan ;
    lexinfo:script :AksaraCacarakan ;
    :jumlahKarakter "{jumlah_karakter}"^^xsd:integer .

:{translit_id} a :Transliterasi ;
    rdf:value "{transliterasi}"@su-Latn ;
    :menggunakanAturan "Aturan Transliterasi Cacarakan-Latin 2025" .

:{terjemah_id} a :Terjemahan ;
    rdf:value "{terjemahan}"@id ;
    :keBahasa "id" ;
    :dariBahasa "su" .
''')

# Contoh pemakaian:
generate_turtle_from_csv("data.csv", "naskah_sunda.ttl")
