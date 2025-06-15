# 📚 Sistem Pencarian Semantik Naskah Sunda Kuno Aksara Cacarakan

Sistem ini merupakan aplikasi berbasis web untuk melakukan pencarian semantik terhadap baris-baris naskah kuno Sunda beraksara Cacarakan yaitu Carita Parahyangan. Dengan menggabungkan teknologi Semantic Web seperti RDF, Ontologi, dan SPARQL, pengguna dapat menelusuri isi naskah berdasarkan aksara asli, transliterasi latin, dan terjemahan Bahasa Indonesia.

---

## 🛠️ Teknologi yang Digunakan

- **RDF (Turtle Format)** untuk representasi data semantik
- **OWL Ontology** untuk skema data (dibuat dengan Protégé)
- **Apache Jena Fuseki** sebagai SPARQL Endpoint
- **Python Streamlit** untuk antarmuka pengguna
- **SPARQL** sebagai bahasa query

---

## 📦 Panduan Instalasi

### 1. Unduh dan Ekstrak Apache Jena Fuseki
- Kunjungi [https://jena.apache.org/download/](https://jena.apache.org/download/)
- Unduh versi Fuseki yang sesuai untuk sistem Anda (ZIP/TAR)
- Ekstrak file ke lokasi yang mudah diakses, misalnya `C:\apache-jena-fuseki`

### 2. Verifikasi Instalasi Java
- Buka terminal / CMD
- Jalankan:
  ```bash
  java -version
  ```
- Pastikan Java 8 atau lebih tinggi sudah terinstal

### 3. Jalankan Fuseki Server
- Navigasi ke direktori hasil ekstrak:
  ```bash
  cd C:\apache-jena-fuseki
  ```
- Jalankan:
  ```bash
  fuseki-server
  ```
- Atau klik `fuseki-server.bat` secara langsung
- Server akan tersedia di: [http://localhost:3030](http://localhost:3030)

---

## 🗂️ Upload Dataset RDF (TTL)

1. Buka browser, akses `http://localhost:3030`
2. Klik **Manage Datasets** → **+ Add new dataset**
3. Isi nama dataset (misal: `CaritaParahyangan`) dan pilih tipe: **Persistent (TDB2)**
4. Setelah dataset dibuat, buka dan klik **Upload data**
5. Pilih file RDF TTL (`output.ttl`) yang telah dibuat dan klik **Upload**

---

## 🔎 Jalankan Query SPARQL

1. Buka dataset `CaritaParahyangan` di Fuseki
2. Klik tab **Query**
3. Gunakan endpoint: `/CaritaParahyangan/sparql`
4. Contoh query:
```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://contoh.org/ontology#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?id ?urutan ?aksara ?transliterasi ?terjemahan
WHERE {
  ?baris a :BarisNaskah ;
         dcterms:identifier ?id ;
         :urutan ?urutan ;
         :mengandungAksara [ rdf:value ?aksara ] ;
         :hasTransliteration [ rdf:value ?transliterasi ] ;
         :hasTranslation [ rdf:value ?terjemahan ] .
}
ORDER BY ASC(?urutan)
```
5. Jalankan dan lihat hasil baris naskah, aksara, transliterasi, serta terjemahannya

---

## 💻 Antarmuka Pencarian (Streamlit)

1. Pastikan Python dan Streamlit sudah terinstal
2. Jalankan aplikasi:
```bash
streamlit run app.py
```
3. Aplikasi akan berjalan di browser di [http://localhost:8501](http://localhost:8501)
4. Anda dapat mencari berdasarkan teks transliterasi atau terjemahan dengan memanfaatkan SPARQL endpoint

---

## 📦 Panduan Penggunaan Aplikasi
Untuk menjalankan aplikasi ini, caranya cukup mudah, ikuti langkah per langkah dibawah berikut ini : 
1. Jalankan Streamlit dengan perintah “streamlit run ‘nama_projek’.py”, misalnya [streamlit run app.py]
2. Berikutnya, biasanya akan otomatis terbuka di browser yaitu ke http://localhost:8501, ini artinya aplikasi sudah berjalan di lokal.
3. Pada menu “Pencarian Umum” masukkan kata kunci pencarian yang ingin dicari (Aksara Cacarakan, Transliterasi, dan Bahasa Indonesia/Terjemahan).
4. Maka akan tampil baris-baris apa saja yang mengandung kata kunci yang dicari serta hasil translasi, transliterasi, dan aksara cacarakannya.
5. Ketika masuk kedalam menu “Pencarian Lanjutan” kita dapat melakukan filter terkait apa yang ingin dicari, Berapa minimal kata yang ingin dicari. Aplikasi Akan Menunjukkan data Yang diinginkan oleh pengguna
6. Selain menu diatas, terdapat menu “Jelajahi Data”, yang digunakan untuk melihat seluruh data, dapat dibuat tampilan untuk 25, 50, 100 data yang akan ditampilkan
7. Selanjutnya terdapat menu “Statistik”. Pada menu ini ditampilkan statistik data seperti berapa jumlah data yang ada, rata-rata panjang kata pada data, jumlah data berdasarkan klasifikasi panjang kata.
8. Terakhir terdapat menu “Pengaturan”, yang berisikan tentang menu check untuk memastikan apakah aplikasi kita sudah terhubung ke dalam server Apache Jena Fuseki.
9. Itulah langkah-langkah sederhana yang merupakan panduan singkat tentang aplikasi web yang kami dibuat.


## 📈 Hasil yang Diharapkan

- ✅ RDF dataset yang merepresentasikan struktur naskah Cacarakan secara semantik
- ✅ Ontologi yang dapat dibuka dan divisualisasikan di Protégé
- ✅ Antarmuka pencarian berbasis web yang menghubungkan pengguna dengan data RDF menggunakan SPARQL
- ✅ Laporan proyek akhir yang menjelaskan arsitektur, desain ontologi, dan evaluasi sistem

---


## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan pembelajaran . Silakan gunakan atau modifikasi dengan menyertakan atribusi yang sesuai.

---

## 👤 Pengembang

> Proyek ini dikembangkan oleh Kelompok 6 sebagai bagian dari tugas akhir mata kuliah *Semantic Web* – Teknik Informatika Unpad 2025.
1. Muhammad Yusuf Adhi Surya - 140810220027
2. Muhammad Nabil Indiharto - 140810220067
3. Devalco Aghazzan Muslion- 140810220079


