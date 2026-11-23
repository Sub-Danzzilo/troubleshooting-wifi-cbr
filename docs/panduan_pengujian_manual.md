# Panduan Pengujian Manual di Papan Tulis

Panduan operasional untuk tim: apa yang dikerjakan saat **pengujian sistem
dengan hitungan manual di papan tulis**, siapa mengerjakan apa, dan angka apa
yang harus muncul. Semua angka di dokumen ini sudah dicek memakai fungsi proyek
sendiri (`core.similarity.hitung_rinci`, `core.cbr_engine.retrieve`,
`core.cbr_engine.retain`), jadi bisa dipakai sebagai patokan saat latihan maupun
saat sidang.

Dokumen pendamping:

- `docs/validasi_manual.md` — tiga contoh hitung tangan yang sudah jadi bahan
  uji pytest.
- `docs/hasil_evaluasi.md` — hasil leave-one-out dan lima skenario (bukan
  pengujian papan tulis).
- `docs/catatan_metodologi.md` — alasan pemilihan CBR, Jaccard, dan bobot.

---

## 1. Apa yang sebenarnya dinilai

Dosen menghitung sendiri perhitungan sistem di papan tulis, lalu
membandingkannya dengan output aplikasi. Karena itu pengujian manual bukan
menguji "apakah diagnosisnya benar", melainkan menguji **apakah perhitungan
sistem bisa dipertanggungjawabkan**:

1. Rumus yang dipakai jelas dan ditulis di papan.
2. Anggota himpunan A (input) dan B (kasus) dapat ditunjukkan, bukan
   disembunyikan.
3. Aritmetika irisan, gabungan, dan pembagiannya benar.
4. Angka di papan **sama** dengan angka di layar (tabel top-3 dan expander
   "Perhitungan rinci").

Tiga hal yang wajib bisa dilakukan setiap anggota:

- [ ] Menuliskan himpunan A dan B dari gejala yang tampil di layar.
- [ ] Menghitung `|A ∩ B| / |A ∪ B|` tanpa melihat catatan.
- [ ] Membuka expander "Perhitungan rinci" dan mencocokkan tiap barisnya dengan
  papan.

---

## 2. Persiapan H-1

### 2.1 Menyiapkan aplikasi

```bash
pip install -r requirements.txt
python -m pytest                  # semua uji harus lulus
streamlit run app.py              # buka http://localhost:8501
```

Wajib sebelum latihan maupun demo:

1. Buka sidebar → **Reset case base** → centang konfirmasi → **Reset Case
   Base**. Tanpa reset, `data/case_base.json` bisa sudah berisi kasus hasil
   retain dari latihan sebelumnya, sehingga daftar kasus di layar berbeda dengan
   lembar contekan.
2. Pastikan sidebar **Mode Similarity = Jaccard biasa** saat mulai. Mode diganti
   di tengah demo hanya kalau memang ingin menunjukkan perbandingan.
3. Pastikan jumlah kasus di sidebar = **15**. Kalau bukan 15, reset belum
   berhasil.

### 2.2 Yang dibawa

- Laptop + adaptor + kabel HDMI, browser di-zoom ±110% agar angka terbaca dari
  jauh.
- Dua tab: aplikasi dan dokumen ini (untuk lembar contekan).
- Spidol 2 warna di papan: satu warna untuk himpunan, satu warna untuk
  aritmetika.
- Cetak **Lampiran A (25 gejala)** dan **Lampiran B (15 kasus)** dari dokumen
  ini, atau buka bagian itu di ponsel.
- Tangkapan layar cadangan hasil tiap demo (untuk laporan artikel bila aplikasi
  bermasalah).

### 2.3 Latihan minimal sekali

Lakukan Demo 1 dan Demo 2 (bagian 5) pada data asli sebelum hari-H, lalu reset
case base. Kalau ada kasus hasil retain yang tidak diinginkan, reset lagi
sebelum demo dimulai.

---

## 3. Pembagian peran (4 orang)

| Peran | Tugas | Jangan dilakukan |
| --- | --- | --- |
| **Operator** | Mengetik/memilih gejala di aplikasi, membuka expander, mengganti mode, menekan tombol simpan | Menjelaskan metode sambil mengetik (bisa salah klik) |
| **Juru tulis papan** | Menulis rumus, himpunan A dan B, irisan, gabungan, pembilang, penyebut, hasil | Menghitung di kepala tanpa menulis langkahnya |
| **Juru bicara** | Menjelaskan alur CBR, menyebut alasan pemilihan Jaccard, menjawab pertanyaan dosen | Mengklaim akurasi dunia nyata |
| **Pemeriksa / timekeeper** | Mencocokkan angka papan dengan layar, menjaga waktu, menyebut langkah berikutnya | Membiarkan angka papan dan layar berbeda tanpa dikoreksi |

Kalau kelompok hanya 3 orang, peran pemeriksa digabung dengan juru tulis papan.

Kalimat pembuka yang aman (10 detik):

> "Sistem ini CBR, bukan rule-based. Pengetahuan disimpan sebagai 15 kasus.
> Keluhan pengguna jadi himpunan gejala, lalu dihitung kemiripannya dengan
> Jaccard. Kami akan hitung manual satu kasus, lalu cocokkan dengan tampilan
> aplikasi."

---

## 4. Format baku tulisan di papan

Selalu tulis dengan urutan yang sama agar dosen mudah mengikuti:

```text
Rumus : J(A,B) = |A ∩ B| / |A ∪ B|

A (input, 6 gejala) = { tidak_connect, semua_perangkat, los_merah,
                        pon_mati, internet_mati, wifi_tidak_muncul }

B (K01, 5 gejala)   = { tidak_connect, semua_perangkat, los_merah,
                        pon_mati, internet_mati }

A ∩ B = { tidak_connect, semua_perangkat, los_merah,
          pon_mati, internet_mati }                  → 5
A ∪ B = A ∩ B + { wifi_tidak_muncul }                → 6

J = 5 / 6 = 0,8333
```

Aturan penulisan:

- Satu baris satu langkah; jangan melompat langsung ke hasil.
- Tulis **jumlah anggota** di kanan setiap himpunan (panah `→ 5`).
- Gejala yang hanya ada di input atau hanya ada di kasus ditulis sebagai selisih
  (`A − B`, `B − A`) supaya jelas asal angka gabungan.
- Hasil akhir 4 angka desimal. Aplikasi memakai titik (`0.8333`), presentasi
  boleh memakai koma (`0,8333`); sebutkan sekali bahwa keduanya nilai yang sama.
- Salah hitung tidak perlu dihapus: coret, tulis ulang, dan sebutkan koreksinya.
  Justru menunjukkan proses.
- Jangan menulis gejala yang tidak dipilih. "Tidak tahu" berarti tidak
  dilaporkan, jadi tidak masuk himpunan A maupun B.

Cara cepat menghitung gabungan tanpa menulis ulang semua anggota:

```text
|A ∪ B| = |A| + |B| − |A ∩ B|
contoh : 6 + 5 − 5 = 6
```

---

## 5. Skenario demo yang sudah dicek

Empat skenario di bawah memakai **gejala yang bisa dipilih di form aplikasi**,
jadi angkanya pasti muncul di layar. Urutan pengerjaan: Demo 1 (Jaccard) → 1b
(Weighted) → Demo 2 → Demo 3 → Demo 4.

### Demo 1 — Kabel fiber, mode Jaccard

Gejala yang dipilih di form:

| Bagian form | Pilihan |
| --- | --- |
| Keluhan utama | Tidak bisa terhubung ke WiFi sama sekali; Gangguan dirasakan di semua perangkat |
| POWER | Tidak tahu |
| PON | Mati |
| LOS | Merah |
| INTERNET | Mati |
| WLAN | Tidak tahu |
| LAN | Tidak tahu |
| Informasi tambahan | (kosong) |
| Tambahan | centang "Nama WiFi tidak muncul di daftar jaringan" |

A = {`tidak_connect`, `semua_perangkat`, `los_merah`, `pon_mati`,
`internet_mati`, `wifi_tidak_muncul`} → 6 anggota

| Kasus | A ∩ B | A ∪ B | Jaccard | Layar |
| --- | --- | --- | --- | --- |
| **K01** {`tidak_connect`, `semua_perangkat`, `los_merah`, `pon_mati`, `internet_mati`} | 5 | 6 | 5 / 6 = **0,8333** | 0.8333 |
| **K04** {`tidak_connect`, `semua_perangkat`, `wifi_tidak_muncul`, `power_mati`, `internet_mati`} | 4 | 7 | 4 / 7 = **0,5714** | 0.5714 |
| **K05** {`tidak_connect`, `semua_perangkat`, `wifi_tidak_muncul`, `router_tidak_punya_indikator`} | 3 | 7 | 3 / 7 = **0,4286** | 0.4286 |

Langkah papan tulis untuk K01 (persis seperti bagian 4). Kesimpulan: kasus
terpilih **K01** kategori `kabel_optik_bermasalah`.

### Demo 1b — Demo 1 diulang dengan mode Weighted Jaccard

Pindahkan sidebar ke **Weighted Jaccard** (tidak perlu input ulang). Skor
berubah:

| Kasus | Σ bobot irisan | Σ bobot gabungan | Weighted | Layar |
| --- | --- | --- | --- | --- |
| **K01** | 1 + 1 + 2 + 2 + 2 = 8 | 8 + 1 (`wifi_tidak_muncul`) = 9 | **0,8889** | 0.8889 |
| **K04** | 2 + 1 + 1 + 1 = 5 | 5 + 2 + 2 + 2 (`los_merah`, `pon_mati`, `power_mati`) = 11 | **0,4545** | 0.4545 |
| **K02** | 2 + 1 + 1 = 4 | 9 + 6,5 − 4 = 11,5 | **0,3478** | 0.3478 |

Poin yang bisa disampaikan: dengan Jaccard K05 ada di top-3, sedangkan pada
Weighted K05 turun ke 3/10 = 0,3000 karena `router_tidak_punya_indikator`
menambah bobot gabungan. Yang berubah adalah **urutan kandidat**, bukan
kesimpulan kategori.

### Demo 2 — Password ditolak (contoh dua mode memberi urutan berbeda)

| Bagian form | Pilihan |
| --- | --- |
| Keluhan utama | Tidak bisa terhubung ke WiFi sama sekali; Gangguan dirasakan di semua perangkat |
| POWER | Menyala |
| PON / LOS / INTERNET / LAN | Tidak tahu |
| WLAN | Menyala |
| Informasi tambahan | Password salah muncul saat menyambung |

A = {`tidak_connect`, `password_ditolak`, `semua_perangkat`, `wlan_nyala`,
`power_nyala`} → 5

| Kasus | A ∩ B | A ∪ B | Jaccard | Σ bobot i / g | Weighted |
| --- | --- | --- | --- | --- | --- |
| **K10** {`tidak_connect`, `password_ditolak`, `hanya_1_perangkat`, `wlan_nyala`, `power_nyala`} | 4 | 6 | 4 / 6 = **0,6667** | 3 / 5 | **0,6000** |
| **K11** {`tidak_connect`, `password_ditolak`, `semua_perangkat`, `wlan_nyala`, `internet_nyala`} | 4 | 6 | 4 / 6 = **0,6667** | 3,5 / 4,5 | **0,7778** |
| **K09** {`tidak_connect`, `semua_perangkat`, `wlan_mati`, `power_nyala`, `internet_nyala`, `pon_nyala`} | 3 | 8 | 3 / 8 = **0,3750** | 2,5 / 7 | **0,3571** |

Rincian Weighted:

| Kasus | Perhitungan |
| --- | --- |
| K10 | irisan = 1 + 1 + 0,5 + 0,5 = 3; gabungan = 3 + 1 (`hanya_1_perangkat`) + 1 (`semua_perangkat`) = 5 → 3/5 |
| K11 | irisan = 1 + 1 + 1 + 0,5 = 3,5; gabungan = 3,5 + 0,5 (`power_nyala`) + 0,5 (`internet_nyala`) = 4,5 → 3,5/4,5 |

Kesimpulan yang harus disebut: Jaccard menghasilkan **seri** 0,6667, aplikasi
memilih **K10** karena urutan kasus pada basis dipertahankan saat skor sama
(sort stabil). Weighted memilih **K11**. Keduanya berkategori `password_salah`,
jadi solusinya tetap pada kategori yang benar.

### Demo 3 — Sinyal lemah di satu perangkat

| Bagian form | Pilihan |
| --- | --- |
| Keluhan utama | Internet lambat / loading lama; Gangguan hanya pada satu perangkat |
| POWER / PON / LOS / INTERNET / LAN | Tidak tahu |
| WLAN | Menyala |
| Informasi tambahan | Sinyal lemah / perangkat jauh dari router / banyak dinding |

A = {`internet_lambat`, `sinyal_lemah`, `hanya_1_perangkat`, `wlan_nyala`} → 4

| Kasus | A ∩ B | A ∪ B | Jaccard | Σ bobot i / g | Weighted |
| --- | --- | --- | --- | --- | --- |
| **K15** {`internet_lambat`, `sinyal_lemah`, `hanya_1_perangkat`, `putus_nyambung`, `wlan_nyala`, `internet_nyala`} | 4 | 6 | 4 / 6 = **0,6667** | 3,5 / 5 | **0,7000** |
| **K14** {`internet_lambat`, `sinyal_lemah`, `semua_perangkat`, `wlan_nyala`} | 3 | 5 | 3 / 5 = **0,6000** | 2,5 / 4,5 | **0,5556** |
| **K12** {`connect_tapi_tanpa_internet`, `hanya_1_perangkat`, `internet_nyala`, `wlan_nyala`} | 2 | 6 | 2 / 6 = **0,3333** | 1,5 / 5 | **0,3000** |

Kesimpulan: **K15** (`sinyal_lemah_interferensi`) peringkat pertama di kedua
mode, **K14** kedua. Ini masuk akal karena K15 juga memuat `hanya_1_perangkat`,
sesuai keluhan "hanya satu perangkat".

> **Penting untuk dicatat tim:** `docs/validasi_manual.md` bagian Skenario 3
> masih menyebut K14 sebagai kasus terpilih, padahal input Skenario 3 memuat
> `hanya_1_perangkat` sehingga aplikasi menampilkan K15 (4/6 = 0,6667) di atas
> K14 (3/5 = 0,6000). Skor pairwise K14 = 3/5 memang benar, jadi uji pytest
> tetap lulus; yang perlu diperbaiki hanya kalimat kesimpulan di dokumen itu.
> Lihat bagian 11.

### Demo 4 — Tidak ada kasus yang cukup mirip

| Bagian form | Pilihan |
| --- | --- |
| Keluhan utama | (kosong) |
| POWER / PON / LOS / INTERNET / WLAN | Tidak tahu |
| LAN | Mati |
| Informasi tambahan | (kosong) |

A = {`lan_mati`} → 1 anggota. Tidak ada kasus awal yang memuat `lan_mati`,
sehingga irisan selalu kosong dan **semua skor 0,0000**. Layar menampilkan
peringatan: skor tertinggi 0,0000% di bawah ambang 30,0%, kasus terdekat tetap
tampil sebagai rujukan.

Alternatif dua gejala yang tidak terduga: A = {`wifi_tidak_muncul`,
`putus_nyambung`}. Kasus terdekat K05: A ∩ B = 1 (`wifi_tidak_muncul`), A ∪ B =
5, hasil 1/5 = **0,2000**. Skor tertinggi tetap di bawah ambang 0,30, jadi
peringatan yang sama muncul.

### Ringkasan empat demo

| Demo | Mode | Top-1 | Skor | Top-3 | Kategori top-1 |
| --- | --- | --- | --- | --- | --- |
| 1 | Jaccard | K01 | 5/6 = 0,8333 | K01, K04, K05 | `kabel_optik_bermasalah` |
| 1b | Weighted | K01 | 8/9 = 0,8889 | K01, K04, K02 | `kabel_optik_bermasalah` |
| 2 | Jaccard | K10 | 4/6 = 0,6667 (seri dengan K11) | K10, K11, K09 | `password_salah` |
| 2 | Weighted | K11 | 3,5/4,5 = 0,7778 | K11, K10, K09 | `password_salah` |
| 3 | Jaccard | K15 | 4/6 = 0,6667 | K15, K14, K12 | `sinyal_lemah_interferensi` |
| 3 | Weighted | K15 | 3,5/5 = 0,7000 | K15, K14, K13 | `sinyal_lemah_interferensi` |
| 4 | keduanya | — | 0,0000 | K01 (skor 0) | peringatan ambang |

---

## 6. Menunjukkan siklus 4R di depan dosen

| Tahap | Yang dilakukan | Yang terlihat di layar |
| --- | --- | --- |
| **Retrieve** | Jalankan Demo 1 | Tabel top-3 dengan skor, banner kasus paling mirip |
| **Reuse** | Buka kartu Rekomendasi Solusi | Langkah bernomor dari K01 + tiga kolom gejala (cocok / hanya input / hanya kasus) |
| **Revise** | Pada Demo 3, pilih "Tidak berhasil" → tombol "Coba Kandidat Berikutnya" | Kandidat bergeser ke K14, metrik "Kandidat 2 dari 15" |
| **Retain** | Pada kandidat yang dianggap berhasil, pilih "Ya, berhasil" → **Simpan ke Basis Kasus** | "Kasus baru K16 ditambahkan. Jumlah kasus menjadi 16." |

Buka expander "Lihat semua kasus" di sidebar: K16 muncul dengan
`sumber = retain`, `jumlah_dipakai = 1`, kategori mengikuti kasus acuan.

Demo **duplikat** (buktikan Retain tidak menggandakan kasus):

1. Ulangi input Demo 1 yang sama, tekan **Jalankan Diagnosis**.
2. K16 sekarang muncul sebagai kasus paling mirip dengan similarity **1.0000**.
3. Pilih "Ya, berhasil" → **Simpan ke Basis Kasus**.
4. Layar menampilkan: "Kasus baru identik dengan K16 (similarity 1.0000). Kasus
   tidak ditambahkan, jumlah_dipakai menjadi 2."

Catatan teknis yang perlu diingat bila dosen bertanya: pengecekan duplikat di
tahap Retain **selalu memakai Jaccard**, walaupun aplikasi sedang berada di mode
Weighted. Alasannya, duplikat berarti himpunan gejala yang identik (similarity =
1,0), dan ambang duplikat hanya terpenuhi oleh himpunan yang sama persis.

---

## 7. Kalau dosen memilih gejala sendiri

Ini yang paling mungkin terjadi. Ikuti prosedur enam langkah, jangan improvisasi
rumus:

1. **Operator** memasukkan gejala pilihan dosen (boleh sebagian saja; "Tidak
   tahu" untuk lampu yang tidak diamati). Catat gejala yang benar-benar
   terpilih.
2. **Operator** membuka expander "Perhitungan rinci" pada kandidat peringkat 1.
3. **Juru tulis** menyalin himpunan A dan B dari expander itu ke papan. Jangan
   menyalin hasilnya dulu — tutup bagian bawah expander atau tulis hasilnya
   belakangan.
4. **Juru tulis** menghitung sendiri irisan, gabungan, dan pembagian.
5. **Pemeriksa** membandingkan hasil papan dengan angka di expander dan di tabel
   top-3. Keduanya harus identik sampai 4 desimal.
6. Bila dosen minta top-3, ulangi langkah 2–5 untuk peringkat 2 dan 3. Tidak
   perlu menghitung 15 kasus.

Tips agar cepat dan tidak salah:

- Hitung **irisan dulu** (gejala yang muncul di kedua himpunan), baru gabungan
  dengan rumus `|A| + |B| − |A ∩ B|`.
- Untuk Weighted, tulis bobot di samping tiap gejala: 0,5 (lampu normal), 1,0
  (keluhan/informasi), 2,0 (lampu menyimpang). Jumlahkan irisan dan gabungan
  terpisah.
- Kalau hasil papan dan layar berbeda, **jangan mengubah angka papan**. Periksa
  tiga hal: (a) ada gejala input yang terlewat dicatat, (b) salah memasukkan
  gejala yang hanya ada di kasus, (c) mode di sidebar berbeda dengan rumus yang
  ditulis.
- Kalau skor tertinggi di bawah 0,30, jelaskan itu bukan error: sistem
  menyatakan tidak ada kasus cukup mirip dan tetap menampilkan kasus terdekat
  sebagai rujukan.

---

## 8. Checklist dan alokasi waktu (total ±12 menit)

| Menit | Kegiatan | Penanggung jawab |
| --- | --- | --- |
| 0–1 | Perkenalan sistem, sebut CBR 4R dan 15 kasus | Juru bicara |
| 1–2 | Tunjukkan form input dan cara memilih gejala lampu | Operator |
| 2–6 | Demo 1: tulis A, B, irisan, gabungan, hasil 5/6; cocokkan dengan layar | Juru tulis + pemeriksa |
| 6–7 | Ganti ke Weighted, tunjukkan 8/9 dan urutan top-3 berubah | Operator + juru bicara |
| 7–9 | Demo 2 atau 3: seri Jaccard vs Weighted, atau Revise ke kandidat berikutnya | Semua |
| 9–11 | Retain: simpan K16, lalu demo duplikat `jumlah_dipakai` naik | Operator |
| 11–12 | Demo 4 (ambang) atau tanya jawab | Juru bicara |

Checklist sebelum mulai:

- [ ] Case base = 15 kasus (sidebar).
- [ ] Mode = Jaccard biasa.
- [ ] Halaman input bersih (tombol "Diagnosis Baru" bila perlu).
- [ ] Lembar contekan 25 gejala dan 15 kasus sudah di tangan.
- [ ] Papan bersih, dua spidol, penghapus.
- [ ] Satu orang memegang dokumen ini dan menyebut langkah berikutnya.

---

## 9. Pertanyaan dosen yang sering muncul

| Pertanyaan | Jawaban singkat |
| --- | --- |
| "Ini rule-based?" | Tidak. Tidak ada IF-THEN gejala → kesimpulan; keputusan diambil dari skor kemiripan kasus. `tests/test_larangan_rule_based.py` memindai kode. |
| "Kenapa Jaccard?" | Data berupa himpunan gejala, rumusnya satu baris, dan bisa dihitung tangan di papan. |
| "Kenapa ada dua mode?" | Weighted memberi bobot lebih besar pada lampu menyimpang (2,0) dan lebih kecil pada lampu normal (0,5). |
| "Kenapa gejala 0-0 tidak dihitung?" | Tidak dilaporkan ≠ dipastikan normal; Jaccard hanya bekerja pada anggota himpunan. |
| "Bagaimana sistem belajar?" | Tahap Retain menambah kasus baru, atau hanya menaikkan `jumlah_dipakai` bila gejalanya identik. |
| "Kenapa skor K13 dan K15 mirip?" | Pola gejalanya hampir sama; case base masih kecil. |
| "Apakah skor 0,83 bagus?" | Skor menunjukkan kemiripan relatif, bukan probabilitas keberhasilan. Yang dipakai adalah urutan kandidat. |
| "Kenapa ada kasus di bawah ambang?" | Case base terbatas; sistem lebih memilih menyatakan tidak yakin daripada memaksa diagnosis. |
| "Bisa ditambah kasus baru tanpa ubah kode?" | Bisa, lewat alur umpan balik (Retain) atau menambah entri di `CASE_BASE_AWAL`. |
| "Berapa akurasinya?" | Leave-one-out 73,3% top-1 Jaccard dan 80,0% Weighted; top-3 93,3% keduanya. Ini konsistensi case base, bukan performa lapangan. |

Kalimat yang **jangan** diucapkan: "sistem ini akurat 80% untuk semua gangguan
WiFi", "sistem lebih baik dari teknisi", "lima skenario membuktikan sistem siap
produksi", "bobot 2,0 adalah bobot optimal".

---

## 10. Troubleshooting saat demo

| Gejala masalah | Penyebab | Solusi cepat |
| --- | --- | --- |
| Jumlah kasus bukan 15 | `data/case_base.json` menyimpan hasil latihan | Sidebar → Reset case base (centang konfirmasi) |
| Angka di layar beda dengan contekan | Mode sidebar bukan Jaccard, atau kasus retain menambah pesaing | Cek mode, reset case base, ulangi diagnosis |
| Peringatan "basis kasus kosong" / error JSON | Berkas JSON rusak | Hapus `data/case_base.json`, muat ulang aplikasi (dibuat ulang dari 15 kasus awal) |
| Tombol simpan tidak muncul | Belum memilih "Ya, berhasil" | Pilih radio umpan balik, baru tombol muncul |
| Halaman hasil kosong | Belum ada input pada sesi ini | Kembali ke input, jalankan diagnosis |
| Port 8501 dipakai proses lain | Instans Streamlit lama masih jalan | Tutup instans lama, atau `streamlit run app.py --server.port 8502` |
| Tema tidak berubah | Streamlit menyimpan tema per proses | Klik "Muat ulang halaman" di sidebar |
| Perhitungan rinci tidak ketemu | Ada di expander di bawah tabel top-3 | Gulir ke bawah, buka "Perhitungan rinci — 1. Kxx" |

---

## 11. Temuan yang sebaiknya dibereskan sebelum DL minggu 15

Ditemukan saat menyusun panduan ini; belum diubah karena menyangkut klaim
metodologi dan angka di laporan. Putuskan bersama tim.

1. **Gejala `internet_mati_total` tidak ada di `DAFTAR_GEJALA` dan
   `BOBOT_GEJALA`.** Gejala ini muncul di K06 dan skenario uji S1/S3, sehingga
   tidak bisa dipilih di form dan bobotnya memakai nilai default 1,0. Akibatnya
   Skenario 1 di `docs/validasi_manual.md` **tidak dapat direproduksi dari UI**.
   Untuk demo, pakai Demo 1 di panduan ini yang seluruh gejalanya bisa dipilih.
   Pilihan perbaikan: tambahkan sebagai gejala resmi (jumlah gejala jadi 26 dan
   skor K06 berubah), atau hapus dari K06/skenario lalu jalankan ulang evaluasi.
2. **Kesimpulan Skenario 3 di `docs/validasi_manual.md` menyebut K14 sebagai
   top-1.** Dengan input yang tertulis di sana, aplikasi menampilkan K15 = 4/6 =
   0,6667 di atas K14 = 3/5 = 0,6000. Skor pairwise K14 tetap benar dan uji
   pytest tetap lulus; yang salah hanya kalimat kesimpulan dan tabelnya (K15
   belum dimasukkan).
3. **`README.md` masih menyebut "tema terang"** pada komentar struktur proyek,
   padahal `.streamlit/config.toml` memakai tema gelap sebagai default.
4. **Jumlah uji pytest** berubah bila tes ditambah; perbarui angka di artikel
   dan `catatan-laporan/ringkasan-proyek-untuk-artikel.md` setelah
   `python -m pytest` dijalankan.
5. **Angka evaluasi berasal dari `CASE_BASE_AWAL`.** Bila demo sudah menambah
   kasus, jalankan ulang `python -m evaluasi.jalankan_evaluasi` sebelum mengutip
   angka.

---

## 12. Template rekap hasil pengujian (bahan artikel)

Isi satu baris per kasus yang dihitung di papan, lalu simpan sebagai bagian
"Hasil Pengujian Manual" di artikel.

| No | Skenario | Gejala input (n) | Kasus | \|A ∩ B\| | \|A ∪ B\| | Jaccard tangan | Jaccard app | Cocok? | Σbobot ∩ / ∪ | Weighted tangan | Weighted app | Cocok? | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Demo 1 | 6 | K01 | 5 | 6 | 0,8333 | 0,8333 | ya | 8 / 9 | 0,8889 | 0,8889 | ya | mode Jaccard & Weighted |
| 2 | | | | | | | | | | | | | |

Aturan pengisian:

- "Cocok?" hanya boleh "ya" bila keempat angka (pembilang, penyebut, hasil, dan
  skor tabel top-3) sama dengan layar.
- Bila ada baris "tidak", tuliskan penyebabnya di kolom Catatan (misalnya salah
  hitung manual, bukan salah aplikasi) dan hitung ulang sampai cocok.

---

## Lampiran A — 25 gejala, label form, dan bobot

| Kode gejala | Label di form | Kelompok | Bobot |
| --- | --- | --- | --- |
| `tidak_connect` | Tidak bisa terhubung ke WiFi sama sekali | A | 1,0 |
| `connect_tapi_tanpa_internet` | Terhubung ke WiFi, tetapi tidak ada akses internet | A | 1,0 |
| `internet_lambat` | Internet lambat / loading lama | A | 1,0 |
| `putus_nyambung` | Koneksi sering putus lalu tersambung lagi | A | 1,0 |
| `semua_perangkat` | Gangguan dirasakan di semua perangkat | A | 1,0 |
| `hanya_1_perangkat` | Gangguan hanya pada satu perangkat | A | 1,0 |
| `wifi_tidak_muncul` | Nama WiFi tidak muncul di daftar jaringan | A | 1,0 |
| `power_nyala` | Lampu POWER menyala normal | B | 0,5 |
| `power_mati` | Lampu POWER mati | B | 2,0 |
| `power_kedip` | Lampu POWER berkedip | B | 2,0 |
| `pon_nyala` | Lampu PON menyala normal | B | 0,5 |
| `pon_mati` | Lampu PON mati | B | 2,0 |
| `pon_kedip` | Lampu PON berkedip | B | 2,0 |
| `los_mati` | Lampu LOS mati (normal) | B | 0,5 |
| `los_merah` | Lampu LOS menyala merah | B | 2,0 |
| `los_kedip` | Lampu LOS berkedip | B | 2,0 |
| `internet_nyala` | Lampu INTERNET menyala normal | B | 0,5 |
| `internet_mati` | Lampu INTERNET mati | B | 2,0 |
| `wlan_nyala` | Lampu WLAN menyala normal | B | 0,5 |
| `wlan_mati` | Lampu WLAN mati | B | 2,0 |
| `lan_nyala` | Lampu LAN menyala normal | B | 0,5 |
| `lan_mati` | Lampu LAN mati | B | 2,0 |
| `router_tidak_punya_indikator` | Router tidak memiliki lampu indikator | C | 1,0 |
| `password_ditolak` | Pesan password salah muncul saat menyambung | C | 1,0 |
| `sinyal_lemah` | Sinyal lemah / perangkat jauh dari router / banyak dinding | C | 1,0 |

## Lampiran B — 15 kasus awal (lembar contekan)

| ID | Kategori | Gejala (n) |
| --- | --- | --- |
| K01 | `kabel_optik_bermasalah` | tidak_connect, semua_perangkat, los_merah, pon_mati, internet_mati (5) |
| K02 | `kabel_optik_bermasalah` | tidak_connect, semua_perangkat, putus_nyambung, internet_lambat, los_merah, pon_nyala (6) |
| K03 | `kabel_optik_bermasalah` | internet_lambat, putus_nyambung, los_kedip, pon_nyala, semua_perangkat (5) |
| K04 | `router_mati_daya` | tidak_connect, semua_perangkat, wifi_tidak_muncul, power_mati, internet_mati (5) |
| K05 | `router_mati_daya` | tidak_connect, semua_perangkat, wifi_tidak_muncul, router_tidak_punya_indikator (4) |
| K06 | `gangguan_isp` | connect_tapi_tanpa_internet, semua_perangkat, **internet_mati_total**, pon_nyala, los_mati, internet_mati (6) |
| K07 | `gangguan_isp` | internet_lambat, semua_perangkat, connect_tapi_tanpa_internet, pon_nyala, internet_nyala (5) |
| K08 | `wlan_nonaktif` | wifi_tidak_muncul, semua_perangkat, wlan_mati, power_nyala, internet_nyala (5) |
| K09 | `wlan_nonaktif` | tidak_connect, semua_perangkat, wlan_mati, power_nyala, internet_nyala, pon_nyala (6) |
| K10 | `password_salah` | tidak_connect, password_ditolak, hanya_1_perangkat, wlan_nyala, power_nyala (5) |
| K11 | `password_salah` | tidak_connect, password_ditolak, semua_perangkat, wlan_nyala, internet_nyala (5) |
| K12 | `masalah_perangkat_klien` | connect_tapi_tanpa_internet, hanya_1_perangkat, internet_nyala, wlan_nyala (4) |
| K13 | `masalah_perangkat_klien` | putus_nyambung, hanya_1_perangkat, internet_lambat, connect_tapi_tanpa_internet, internet_nyala (5) |
| K14 | `sinyal_lemah_interferensi` | internet_lambat, sinyal_lemah, semua_perangkat, wlan_nyala (4) |
| K15 | `sinyal_lemah_interferensi` | internet_lambat, sinyal_lemah, hanya_1_perangkat, putus_nyambung, wlan_nyala, internet_nyala (6) |

`internet_mati_total` pada K06 ditebalkan karena tidak tersedia di form (lihat
bagian 11).
