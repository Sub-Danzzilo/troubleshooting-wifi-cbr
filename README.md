# Sistem Pakar Troubleshooting WiFi (CBR)

Proyek kelompok mata kuliah **Kecerdasan Buatan**. Sistem pakar yang mendiagnosis
masalah WiFi rumah dengan **Case-Based Reasoning (CBR)**: keluhan baru dicocokkan
ke kasus-kasus lama yang paling mirip, lalu solusinya direkomendasikan dan sistem
belajar dari umpan balik pengguna.

> Status: kerangka proyek. Bagian bertanda **(TODO)** diisi setelah kode dan evaluasi selesai.

## Fitur

- Input gejala: keluhan utama, status lampu router (POWER, PON, LOS, INTERNET, WLAN, LAN), info tambahan
- Top-3 kasus paling mirip dengan skor similarity dan penjelasan gejala yang cocok
- Rekomendasi solusi + confidence bar
- Feedback pengguna, lalu kasus baru disimpan ke case base (siklus 4R lengkap)
- Pilihan Jaccard biasa atau Weighted Jaccard
- Case base persisten di JSON
- Perhitungan rinci per kasus untuk validasi manual

## Cara Menjalankan

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Uji dan evaluasi:

```bash
python -m pytest
python -m evaluasi.jalankan_evaluasi
```

## Alur CBR (Siklus 4R)

| Tahap | Fungsi | Yang terjadi |
|---|---|---|
| **Retrieve** | `retrieve()` | Hitung similarity gejala baru terhadap semua kasus, ambil top-3. Jika skor terbaik di bawah ambang, sistem menyatakan tidak ada kasus yang cukup mirip. |
| **Reuse** | `reuse()` | Ambil solusi kasus terpilih apa adanya, sertakan selisih gejala sebagai hal yang perlu diverifikasi. |
| **Revise** | `revise()` | Tanyakan apakah solusi berhasil. Jika tidak, coba kandidat berikutnya; jika semua gagal, pengguna dapat mengisi solusi yang akhirnya berhasil. |
| **Retain** | `retain()` | Simpan sebagai kasus baru, atau hanya naikkan `jumlah_dipakai` bila duplikat. Disimpan ke `data/case_base.json`. |

## Similarity

**Jaccard:** `|A ∩ B| / |A ∪ B|`

**Weighted Jaccard:** jumlah bobot gejala di irisan dibagi jumlah bobot gejala di gabungan.
Bobot (`BOBOT_GEJALA`) memberi nilai lebih pada gejala pembeda (misal `los_merah`) dan
lebih kecil pada gejala kondisi normal yang muncul di hampir semua kasus (misal `los_mati`).
Bobot adalah parameter similarity, bukan aturan inferensi.

### Catatan metodologi

- Jaccard mengabaikan pasangan sama-sama False (0-0). "Gejala tidak dipilih" berarti
  *tidak dilaporkan*, bukan kecocokan. **(TODO: lengkapi kelebihan dan kekurangannya.)**
- Setiap lampu punya opsi "Tidak tahu" yang tidak menambah gejala apa pun.
- Representasi one-hot memecah pilihan lampu yang saling eksklusif menjadi fitur terpisah.
  Alternatifnya adalah similarity per-atribut (lihat Pengembangan Lanjutan).

## Validasi Manual

Pengujian dilakukan dengan menghitung similarity **dengan tangan** lalu mencocokkannya dengan output
aplikasi. Aplikasi menyediakan expander "Lihat perhitungan rinci" yang menampilkan himpunan gejala,
irisan, gabungan, dan rumus dengan angka terisi. Contoh perhitungan ada di
[`docs/validasi_manual.md`](docs/validasi_manual.md).

## Mengapa CBR, Bukan Rule-Based

- Pengetahuan troubleshooting secara alami berbentuk **pengalaman kasus**, bukan aturan lengkap.
- Pakar tidak perlu merumuskan seluruh aturan di awal.
- Sistem **belajar** lewat tahap Retain.
- Keputusan **transparan**: ada kasus rujukan, skor, dan gejala yang cocok.
- Status lampu router diperlakukan sebagai **atribut kasus**, bukan pemicu aturan.

Keterbatasan: kualitas hasil bergantung pada cakupan case base dan pemilihan bobot.

## Struktur Proyek

```
.
├── app.py                  # Entry point Streamlit
├── AGENTS.md               # Panduan untuk AI agent
├── core/
│   ├── case_base.py        # Gejala, bobot, parameter, 15 kasus awal
│   ├── similarity.py       # Jaccard, Weighted Jaccard, perbandingan gejala
│   ├── cbr_engine.py       # retrieve, reuse, revise, retain
│   └── storage.py          # Muat/simpan/reset case base JSON
├── ui/
│   ├── halaman_input.py    # Halaman input gejala
│   ├── halaman_hasil.py    # Halaman hasil diagnosis + feedback
│   ├── sidebar.py          # Sidebar
│   └── komponen.py         # Komponen tampilan bersama
├── evaluasi/
│   ├── skenario_uji.py     # 5 skenario uji baru
│   └── jalankan_evaluasi.py
├── tests/                  # Uji similarity + penjaga larangan rule-based
├── docs/                   # Catatan metodologi, hasil evaluasi, validasi manual
├── data/                   # case_base.json (dibuat otomatis)
└── requirements.txt
```

## Evaluasi

**(TODO)** Isi setelah `python -m evaluasi.jalankan_evaluasi` dijalankan:

- Akurasi leave-one-out (top-1, top-3): Jaccard vs Weighted Jaccard
- Akurasi 5 skenario baru
- Analisis kasus yang salah

Detail ada di `docs/hasil_evaluasi.md`.

## Alur Layar (untuk demo)

**(TODO)** Tambahkan screenshot atau deskripsi untuk tiga skenario: kasus berhasil di-retain,
kasus duplikat, dan kasus tanpa kecocokan (di bawah ambang).

## Pengembangan Lanjutan

- Similarity per-atribut (attribute-value) dengan local similarity per lampu
- Bobot dari pakar atau hasil optimasi dari data
- Aturan adaptasi berbasis kasus (tanpa if-then)
- Indeksasi/pengelompokan case base untuk retrieval lebih cepat
- Menambah gejala, misalnya `connect_tapi_tanpa_internet`

## Tim

**(TODO)** Nama anggota, NIM, kelas, dosen pengampu.
