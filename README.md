# Sistem Pakar Troubleshooting WiFi (CBR)

Proyek kelompok mata kuliah **Kecerdasan Buatan**. Sistem pakar yang
mendiagnosis masalah WiFi rumah dengan **Case-Based Reasoning (CBR)**: keluhan
baru dicocokkan ke kasus-kasus lama yang paling mirip, lalu solusinya
direkomendasikan dan sistem belajar dari umpan balik pengguna.

## Fitur

- Input gejala: keluhan utama, status lampu router (POWER, PON, LOS, INTERNET,
  WLAN, LAN), info tambahan
- Top-3 kasus paling mirip dengan skor similarity dan penjelasan gejala yang
  cocok
- Rekomendasi solusi + confidence bar
- Feedback pengguna, lalu kasus baru disimpan ke case base (siklus 4R lengkap)
- Pilihan Jaccard biasa atau Weighted Jaccard
- Case base persisten di `data/case_base.json` dan bisa di-reset dari sidebar
- Tampilan gelap secara default, bisa diganti ke terang lewat sidebar
- Perhitungan rinci per kasus untuk validasi manual (himpunan, irisan, gabungan,
  pembilang, penyebut)

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

Evaluasi menulis ulang `docs/hasil_evaluasi.md` dengan tabel akurasi, daftar
kasus yang salah, dan perhitungan rinci tiap skenario.

## Alur CBR (Siklus 4R)

| Tahap | Fungsi | Yang terjadi |
| --- | --- | --- |
| **Retrieve** | `retrieve()` | Hitung similarity gejala baru terhadap semua kasus, urutkan menurun. Jika skor terbaik di bawah `AMBANG_MIN_SIMILARITY` (0,30), sistem menyatakan tidak ada kasus yang cukup mirip. |
| **Reuse** | `reuse()` | Ambil solusi kasus terpilih apa adanya, sertakan selisih gejala sebagai hal yang perlu diverifikasi. |
| **Revise** | `revise()` | Tanyakan apakah solusi berhasil. Jika tidak, coba kandidat berikutnya; jika semua gagal, pengguna dapat mengisi solusi yang akhirnya berhasil. |
| **Retain** | `retain()` | Simpan sebagai kasus baru, atau hanya naikkan `jumlah_dipakai` bila duplikat (similarity >= 1,0). Disimpan ke `data/case_base.json`. |

Basis pengetahuan berupa **15 kasus** pada `CASE_BASE_AWAL`, bukan kumpulan
aturan. Status lampu router hanya menjadi atribut di dalam kasus.

## Similarity

**Jaccard:** `|A ∩ B| / |A ∪ B|`

**Weighted Jaccard:** jumlah bobot gejala di irisan dibagi jumlah bobot gejala
di gabungan.

| Kelompok gejala | Bobot |
| --- | --- |
| Keluhan utama dan informasi tambahan | 1,0 |
| Lampu kondisi normal (`power_nyala`, `pon_nyala`, `los_mati`, `internet_nyala`, `wlan_nyala`, `lan_nyala`) | 0,5 |
| Lampu menyimpang (`power_mati`, `los_merah`, `los_kedip`, `pon_mati`, `internet_mati`, `wlan_mati`, `lan_mati`) | 2,0 |

Bobot adalah parameter similarity, bukan aturan inferensi. Semua ambang dan
bobot hanya didefinisikan di `core/case_base.py`.

### Catatan metodologi

- Jaccard mengabaikan pasangan sama-sama False (0-0). "Gejala tidak dipilih"
  berarti *tidak dilaporkan*, bukan kecocokan. Kelebihan dan kekurangannya
  dibahas di [`docs/catatan_metodologi.md`](docs/catatan_metodologi.md).
- Setiap lampu punya opsi "Tidak tahu" yang tidak menambah gejala apa pun.
- Representasi one-hot memecah pilihan lampu yang saling eksklusif menjadi fitur
  terpisah. Alternatifnya adalah similarity per-atribut (lihat Pengembangan
  Lanjutan).

## Validasi Manual

Pengujian dilakukan dengan menghitung similarity **dengan tangan** lalu
mencocokkannya dengan output aplikasi. Aplikasi menyediakan expander "Lihat
perhitungan rinci" yang menampilkan himpunan gejala, irisan, gabungan, dan rumus
dengan angka terisi. Tiga contoh perhitungan lengkap ada di
[`docs/validasi_manual.md`](docs/validasi_manual.md) dan dipakai sebagai uji
pytest. Langkah praktis untuk tim saat demo/sidang (pembagian peran, urutan
menulis di papan, skenario yang sudah terverifikasi, lembar contekan 25 gejala
dan 15 kasus) ada di
[`docs/panduan_pengujian_manual.md`](docs/panduan_pengujian_manual.md).

## Hasil Evaluasi

Dijalankan dengan `python -m evaluasi.jalankan_evaluasi` (data:
`CASE_BASE_AWAL`, bukan kasus hasil retain). Detail dan perhitungan rinci ada di
[`docs/hasil_evaluasi.md`](docs/hasil_evaluasi.md).

| Pengujian | Mode | Akurasi top-1 | Akurasi top-3 |
| --- | --- | --- | --- |
| Leave-one-out (15 kasus) | Jaccard | 73,3% | 93,3% |
| Leave-one-out (15 kasus) | Weighted Jaccard | 80,0% | 93,3% |
| 5 skenario baru | Jaccard | 100,0% | 100,0% |
| 5 skenario baru | Weighted Jaccard | 100,0% | 100,0% |

Analisis singkat:

- Kesalahan Jaccard: K01 terbaca K04 (kasus K01 tidak memuat
  `internet_mati_total`, sehingga irisan dengan K04 lebih besar), K07 terbaca
  K03, dan pasangan K13/K15 saling tertukar.
- Kesalahan Weighted: K07 terbaca K13, serta pasangan K13/K15 saling tertukar.
  Weighted memperbaiki K01 karena `los_merah` berbobot 2,0.
- K13 (`masalah_perangkat_klien`) dan K15 (`sinyal_lemah_interferensi`) memiliki
  pola gejala yang hampir sama; pembedanya terutama `sinyal_lemah` (K15 juga
  memuat `wlan_nyala`). Pada case base kecil, selisih satu-dua gejala langsung
  mengubah peringkat.
- Lima skenario baru semuanya benar karena dibuat dari pola gejala yang mirip
  dengan kasus awal. Hasil ini menunjukkan konsistensi case base, bukan jaminan
  performa pada keluhan nyata.

## Mengapa CBR, Bukan Rule-Based

- Pengetahuan troubleshooting secara alami berbentuk **pengalaman kasus**, bukan
  aturan lengkap.
- Pakar tidak perlu merumuskan seluruh aturan di awal.
- Sistem **belajar** lewat tahap Retain.
- Keputusan **transparan**: ada kasus rujukan, skor, dan gejala yang cocok.
- Status lampu router diperlakukan sebagai **atribut kasus**, bukan pemicu
  aturan.

Keterbatasan: kualitas hasil bergantung pada cakupan case base dan pemilihan
bobot. `tests/test_larangan_rule_based.py` memastikan tidak ada sisa pola
rule-based di kode.

## Struktur Proyek

```text
.
├── app.py                  # Entry point Streamlit (state + router halaman)
├── assets/logo.svg         # Logo aplikasi
├── .streamlit/config.toml  # Tema terang dengan aksen teal
├── AGENTS.md               # Panduan untuk AI agent dan anggota tim
├── core/
│   ├── case_base.py        # 25 gejala, bobot, parameter, 15 kasus awal
│   ├── similarity.py       # Jaccard, Weighted Jaccard, perbandingan gejala, hitung_rinci
│   ├── cbr_engine.py       # retrieve, reuse, revise, retain
│   └── storage.py          # Muat/simpan/reset case base JSON
├── ui/
│   ├── halaman_input.py    # Halaman input gejala
│   ├── halaman_hasil.py    # Halaman hasil diagnosis + feedback
│   ├── sidebar.py          # Sidebar: mode, daftar kasus, reset
│   └── komponen.py         # Komponen tampilan bersama
├── evaluasi/
│   ├── skenario_uji.py     # 5 skenario uji baru
│   └── jalankan_evaluasi.py
├── tests/                  # Uji similarity, siklus 4R, penjaga larangan rule-based
├── docs/                   # Catatan metodologi, hasil evaluasi, validasi manual
├── data/                   # case_base.json (dibuat otomatis, di-gitignore)
└── requirements.txt
```

## Alur Layar (untuk demo sidang)

1. **Kasus berhasil di-retain** — Masukkan keluhan yang cocok dengan sebuah
   kasus, tekan Diagnosis, pilih "Ya, berhasil", lalu "Simpan ke Basis Kasus".
   Pesan sukses menyebut kasus baru (misalnya K16) dan jumlah kasus bertambah.
2. **Kasus duplikat** — Ulangi diagnosis dengan gejala identik, lalu simpan.
   Pesan berubah menjadi "kasus identik, tidak ditambahkan" dan `jumlah_dipakai`
   kasus lama naik.
3. **Tidak ada kecocokan** — Pilih gejala yang tidak mirip kasus mana pun.
   Muncul peringatan skor tertinggi di bawah ambang; kasus terdekat tetap tampil
   sebagai rujukan, dan pengguna bisa mencoba kandidat berikutnya atau menyimpan
   solusinya sendiri.

## Pengembangan Lanjutan

- Similarity per-atribut (attribute-value) dengan local similarity per lampu
- Bobot dari pakar atau hasil optimasi dari data
- Indeksasi/pengelompokan case base untuk retrieval lebih cepat
- Menambah gejala yang lebih rinci, misalnya jumlah perangkat terhubung atau
  tingkat kebisingan channel
- Menambah kasus awal agar pasangan kategori yang mirip (K13/K15) lebih mudah
  dibedakan

## Tim

Proyek kelompok mata kuliah Kecerdasan Buatan.
