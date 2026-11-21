# Validasi Manual (Hitungan Papan Tulis)

Dokumen ini berisi perhitungan similarity yang dikerjakan **dengan tangan**, lalu
dicocokkan dengan output aplikasi. Angka di sini juga dipakai sebagai uji pytest di
`tests/test_similarity.py`.

## Rumus

**Jaccard:** `similarity = |A ∩ B| / |A ∪ B|`

**Weighted Jaccard:** `similarity = Σ bobot (A ∩ B) / Σ bobot (A ∪ B)`

A = himpunan gejala input pengguna, B = himpunan gejala pada kasus di case base.
Bobot yang dipakai: keluhan = 1,0; lampu menyala/mati normal (`power_nyala`,
`pon_nyala`, `los_mati`, `internet_nyala`, `wlan_nyala`, `lan_nyala`) = 0,5;
lampu menyimpang (`power_mati`, `los_merah`, `internet_mati`, dan sejenisnya) = 2,0.

## Skenario 1 — Kabel fiber terganggu

Keluhan: semua perangkat tidak bisa internet, lampu LOS merah, PON mati.

**A** = {`tidak_connect`, `semua_perangkat`, `internet_mati_total`, `los_merah`, `pon_mati`} → 5 anggota

| Kasus | A ∩ B | A ∪ B | Jaccard | Σ bobot irisan / gabungan | Weighted |
|---|---|---|---|---|---|
| **K01** {`tidak_connect`, `semua_perangkat`, `los_merah`, `pon_mati`, `internet_mati`} | 4 | 6 | 4 / 6 = **0,6667** | 6 / 9 | **0,6667** |
| **K02** {`tidak_connect`, `semua_perangkat`, `putus_nyambung`, `internet_lambat`, `los_merah`, `pon_nyala`} | 3 | 8 | 3 / 8 = **0,3750** | 4 / 9,5 | **0,4211** |
| **K05** {`tidak_connect`, `semua_perangkat`, `wifi_tidak_muncul`, `router_tidak_punya_indikator`} | 2 | 7 | 2 / 7 = **0,2857** | 2 / 9 | **0,2222** |
| **K04** {`tidak_connect`, `semua_perangkat`, `wifi_tidak_muncul`, `power_mati`, `internet_mati`} | 2 | 8 | 2 / 8 = **0,2500** | 2 / 12 | **0,1667** |
| **K06** {`connect_tapi_tanpa_internet`, `semua_perangkat`, `internet_mati_total`, `pon_nyala`, `los_mati`, `internet_mati`} | 2 | 9 | 2 / 9 = **0,2222** | 2 / 11 | **0,1818** |

Rincian Weighted untuk K01:

| Langkah | Hasil |
|---|---|
| Σ bobot irisan = 1 + 1 + 2 + 2 | 6 |
| Σ bobot gabungan = 6 + 2 (`internet_mati`) + 1 (`internet_mati_total`) | 9 |
| Weighted Jaccard | 6 / 9 = **0,6667** |

Kesimpulan manual: kasus terpilih **K01** (kategori `kabel_optik_bermasalah`) pada kedua mode.
Urutan top-3 sama untuk Jaccard dan Weighted: K01, K02, K05. K05 hanya berbagi dua gejala
dengan input, tetapi tidak membawa gejala lampu normal yang menambah bobot gabungan.
K04 dan K06 disertakan sebagai pembanding di luar top-3.

## Skenario 2 — Password WiFi ditolak

Keluhan: tidak bisa terhubung, muncul pesan password salah, WLAN dan POWER menyala.

**A** = {`tidak_connect`, `password_ditolak`, `semua_perangkat`, `wlan_nyala`, `power_nyala`} → 5 anggota

| Kasus | A ∩ B | A ∪ B | Jaccard | Σ bobot irisan / gabungan | Weighted |
|---|---|---|---|---|---|
| **K10** {`tidak_connect`, `password_ditolak`, `hanya_1_perangkat`, `wlan_nyala`, `power_nyala`} | 4 | 6 | 4 / 6 = **0,6667** | 3 / 5 | **0,6000** |
| **K11** {`tidak_connect`, `password_ditolak`, `semua_perangkat`, `wlan_nyala`, `internet_nyala`} | 4 | 6 | 4 / 6 = **0,6667** | 3,5 / 4,5 | **0,7778** |
| **K09** {`tidak_connect`, `semua_perangkat`, `wlan_mati`, `power_nyala`, `internet_nyala`, `pon_nyala`} | 3 | 8 | 3 / 8 = **0,3750** | 2,5 / 7 | **0,3571** |

Rincian Weighted untuk K11:

| Langkah | Hasil |
|---|---|
| Σ bobot irisan = 1 + 1 + 1 + 0,5 (`wlan_nyala`) | 3,5 |
| Σ bobot gabungan = 3,5 + 0,5 (`internet_nyala`) + 0,5 (`power_nyala`) | 4,5 |
| Weighted Jaccard | 3,5 / 4,5 = **0,7778** |

Kesimpulan manual: Jaccard menghasilkan **seri** 0,6667 antara K10 dan K11, sehingga aplikasi
memilih K10 karena urutan kasus (sort stabil). Weighted Jaccard memilih **K11**. Keduanya
berkategori `password_salah`, jadi rekomendasi solusi tetap pada kategori yang benar.

## Skenario 3 — Sinyal lemah

Keluhan: internet lambat, sinyal lemah, hanya satu perangkat yang terdampak, lampu WLAN menyala.

**A** = {`internet_lambat`, `sinyal_lemah`, `hanya_1_perangkat`, `wlan_nyala`} → 4 anggota

| Kasus | A ∩ B | A ∪ B | Jaccard | Σ bobot irisan / gabungan | Weighted |
|---|---|---|---|---|---|
| **K14** {`internet_lambat`, `sinyal_lemah`, `semua_perangkat`, `wlan_nyala`} | 3 | 5 | 3 / 5 = **0,6000** | 2,5 / 4,5 | **0,5556** |
| **K12** {`connect_tapi_tanpa_internet`, `hanya_1_perangkat`, `internet_nyala`, `wlan_nyala`} | 2 | 6 | 2 / 6 = **0,3333** | 1,5 / 5 | **0,3000** |
| **K13** {`putus_nyambung`, `hanya_1_perangkat`, `internet_lambat`, `connect_tapi_tanpa_internet`, `internet_nyala`} | 2 | 7 | 2 / 7 = **0,2857** | 2 / 6 | **0,3333** |

Rincian Weighted untuk K14:

| Langkah | Hasil |
|---|---|
| Σ bobot irisan = 1 + 1 + 0,5 (`wlan_nyala`) | 2,5 |
| Σ bobot gabungan = 2,5 + 1 (`semua_perangkat`) + 1 (`hanya_1_perangkat`) | 4,5 |
| Weighted Jaccard | 2,5 / 4,5 = **0,5556** |

Kesimpulan manual: kasus terpilih **K14** (kategori `sinyal_lemah_interferensi`) pada kedua mode.
Urutan Weighted: K14, K13, K12 (K13 naik karena `hanya_1_perangkat` dan `putus_nyambung` berbobot 1).

## Mencocokkan dengan Aplikasi

1. Masukkan gejala yang sama seperti himpunan A di halaman input.
2. Tekan **Diagnosis**.
3. Buka expander **"Lihat perhitungan rinci"** pada tiap kasus top-3. Aplikasi menampilkan
   himpunan A, B, irisan, gabungan, pembilang, penyebut, dan hasil dengan angka yang sama
   seperti tabel di atas (format 4 angka desimal).
4. Ganti mode **Jaccard / Weighted Jaccard** di sidebar; skor di tabel top-3 dan di
   perhitungan rinci dihitung oleh fungsi yang sama, jadi harus selalu identik.

## Uji Pytest yang Mewakili Dokumen Ini

| Uji | Isi |
|---|---|
| `test_skenario_1_jaccard_dan_weighted` | K01: 4/6 dan 6/9 |
| `test_skenario_1_kasus_pembanding` | K04: 3/7 dan 4/10; K06: 3/8 dan 4/9 |
| `test_skenario_2_jaccard_seri_dan_weighted` | K10/K11: 4/6, weighted 3/5 dan 3,5/4,5 |
| `test_skenario_3_jaccard_dan_weighted` | K14: 3/5 dan 2,5/4,5 |

## Latihan Sidang

- [ ] Setiap anggota bisa menghitung Jaccard satu pasang kasus tanpa melihat catatan.
- [ ] Bisa menjelaskan kenapa gejala yang tidak dipilih tidak ikut dihitung (pasangan 0-0).
- [ ] Bisa menunjukkan bagian "perhitungan rinci" di aplikasi dan mencocokkannya dengan papan tulis.
- [ ] Tabel ringkas 15 kasus (ID + gejala) sudah disiapkan sebagai contekan.
