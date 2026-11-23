# Hasil Evaluasi

Dibuat otomatis oleh `python -m evaluasi.jalankan_evaluasi` pada 2026-11-24.
Sumber data: `CASE_BASE_AWAL` (15 kasus), bukan `data/case_base.json`, agar
kasus hasil retain tidak memengaruhi hasil.

## Ringkasan

| Pengujian | Mode | Akurasi top-1 | Akurasi top-3 |
| --- | --- | --- | --- |
| Leave-one-out | Jaccard | 73.3% | 93.3% |
| Leave-one-out | Weighted Jaccard | 80.0% | 93.3% |
| 5 skenario baru | Jaccard | 100.0% | 100.0% |
| 5 skenario baru | Weighted Jaccard | 100.0% | 100.0% |

## 1. Leave-one-out (15 kasus)

### Jaccard — leave-one-out

| Kasus uji | Kategori sebenarnya | Top-1 | Skor top-1 | Kategori top-1 | Top-1 benar | Top-3 benar |
| --- | --- | --- | --- | --- | --- | --- |
| K01 | kabel_optik_bermasalah | K04 | 0.4286 | router_mati_daya | tidak | ya |
| K02 | kabel_optik_bermasalah | K03 | 0.5714 | kabel_optik_bermasalah | ya | ya |
| K03 | kabel_optik_bermasalah | K02 | 0.5714 | kabel_optik_bermasalah | ya | ya |
| K04 | router_mati_daya | K05 | 0.5000 | router_mati_daya | ya | ya |
| K05 | router_mati_daya | K04 | 0.5000 | router_mati_daya | ya | ya |
| K06 | gangguan_isp | K07 | 0.3750 | gangguan_isp | ya | ya |
| K07 | gangguan_isp | K03 | 0.4286 | kabel_optik_bermasalah | tidak | tidak |
| K08 | wlan_nonaktif | K09 | 0.5714 | wlan_nonaktif | ya | ya |
| K09 | wlan_nonaktif | K08 | 0.5714 | wlan_nonaktif | ya | ya |
| K10 | password_salah | K11 | 0.4286 | password_salah | ya | ya |
| K11 | password_salah | K10 | 0.4286 | password_salah | ya | ya |
| K12 | masalah_perangkat_klien | K13 | 0.5000 | masalah_perangkat_klien | ya | ya |
| K13 | masalah_perangkat_klien | K15 | 0.5714 | sinyal_lemah_interferensi | tidak | ya |
| K14 | sinyal_lemah_interferensi | K15 | 0.4286 | sinyal_lemah_interferensi | ya | ya |
| K15 | sinyal_lemah_interferensi | K13 | 0.5714 | masalah_perangkat_klien | tidak | ya |

### Weighted Jaccard — leave-one-out

| Kasus uji | Kategori sebenarnya | Top-1 | Skor top-1 | Kategori top-1 | Top-1 benar | Top-3 benar |
| --- | --- | --- | --- | --- | --- | --- |
| K01 | kabel_optik_bermasalah | K02 | 0.3810 | kabel_optik_bermasalah | ya | ya |
| K02 | kabel_optik_bermasalah | K03 | 0.4118 | kabel_optik_bermasalah | ya | ya |
| K03 | kabel_optik_bermasalah | K02 | 0.4118 | kabel_optik_bermasalah | ya | ya |
| K04 | router_mati_daya | K05 | 0.3750 | router_mati_daya | ya | ya |
| K05 | router_mati_daya | K04 | 0.3750 | router_mati_daya | ya | ya |
| K06 | gangguan_isp | K07 | 0.3333 | gangguan_isp | ya | ya |
| K07 | gangguan_isp | K13 | 0.4167 | masalah_perangkat_klien | tidak | tidak |
| K08 | wlan_nonaktif | K09 | 0.6154 | wlan_nonaktif | ya | ya |
| K09 | wlan_nonaktif | K08 | 0.6154 | wlan_nonaktif | ya | ya |
| K10 | password_salah | K11 | 0.4545 | password_salah | ya | ya |
| K11 | password_salah | K10 | 0.4545 | password_salah | ya | ya |
| K12 | masalah_perangkat_klien | K13 | 0.5000 | masalah_perangkat_klien | ya | ya |
| K13 | masalah_perangkat_klien | K15 | 0.5833 | sinyal_lemah_interferensi | tidak | ya |
| K14 | sinyal_lemah_interferensi | K15 | 0.4167 | sinyal_lemah_interferensi | ya | ya |
| K15 | sinyal_lemah_interferensi | K13 | 0.5833 | masalah_perangkat_klien | tidak | ya |

## 2. Lima skenario baru

### Jaccard — 5 skenario baru

| Skenario | Deskripsi | Kategori harapan | Top-1 | Skor | Kategori top-1 | Top-1 benar | Top-3 benar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Kabel fiber terganggu, semua perangkat tidak bisa internet | kabel_optik_bermasalah | K01 | 0.6667 | kabel_optik_bermasalah | ya | ya |
| S2 | Router tidak menyala setelah listrik padam | router_mati_daya | K04 | 0.8000 | router_mati_daya | ya | ya |
| S3 | Lampu PON normal tetapi tidak ada akses internet sama sekali | gangguan_isp | K06 | 0.8333 | gangguan_isp | ya | ya |
| S4 | Nama WiFi hilang karena lampu WLAN mati | wlan_nonaktif | K08 | 0.8000 | wlan_nonaktif | ya | ya |
| S5 | Password WiFi ditolak di semua perangkat setelah diganti | password_salah | K10 | 0.6667 | password_salah | ya | ya |

### Weighted Jaccard — 5 skenario baru

| Skenario | Deskripsi | Kategori harapan | Top-1 | Skor | Kategori top-1 | Top-1 benar | Top-3 benar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Kabel fiber terganggu, semua perangkat tidak bisa internet | kabel_optik_bermasalah | K01 | 0.6667 | kabel_optik_bermasalah | ya | ya |
| S2 | Router tidak menyala setelah listrik padam | router_mati_daya | K04 | 0.7143 | router_mati_daya | ya | ya |
| S3 | Lampu PON normal tetapi tidak ada akses internet sama sekali | gangguan_isp | K06 | 0.9167 | gangguan_isp | ya | ya |
| S4 | Nama WiFi hilang karena lampu WLAN mati | wlan_nonaktif | K08 | 0.9000 | wlan_nonaktif | ya | ya |
| S5 | Password WiFi ditolak di semua perangkat setelah diganti | password_salah | K11 | 0.7778 | password_salah | ya | ya |

## 3. Kasus yang salah

- Jaccard — kasus uji K01 (kabel_optik_bermasalah): top-1 K04 (router_mati_daya,
  skor 0.4286)
- Jaccard — kasus uji K07 (gangguan_isp): top-1 K03 (kabel_optik_bermasalah,
  skor 0.4286)
- Jaccard — kasus uji K13 (masalah_perangkat_klien): top-1 K15
  (sinyal_lemah_interferensi, skor 0.5714)
- Jaccard — kasus uji K15 (sinyal_lemah_interferensi): top-1 K13
  (masalah_perangkat_klien, skor 0.5714)
- Weighted Jaccard — kasus uji K07 (gangguan_isp): top-1 K13
  (masalah_perangkat_klien, skor 0.4167)
- Weighted Jaccard — kasus uji K13 (masalah_perangkat_klien): top-1 K15
  (sinyal_lemah_interferensi, skor 0.5833)
- Weighted Jaccard — kasus uji K15 (sinyal_lemah_interferensi): top-1 K13
  (masalah_perangkat_klien, skor 0.5833)

## 4. Perhitungan rinci skenario (Jaccard)

### S1 — Kabel fiber terganggu, semua perangkat tidak bisa internet

- **Top-1 K01**: A ∩ B = {los_merah, pon_mati, semua_perangkat, tidak_connect}
  (4 anggota), A ∪ B = {internet_mati, internet_mati_total, los_merah, pon_mati,
  semua_perangkat, tidak_connect} (6 anggota) → 4 / 6 = **0.6667**
- **Top-2 K02**: A ∩ B = {los_merah, semua_perangkat, tidak_connect} (3
  anggota), A ∪ B = {internet_lambat, internet_mati_total, los_merah, pon_mati,
  pon_nyala, putus_nyambung, semua_perangkat, tidak_connect} (8 anggota) → 3 / 8
  = **0.3750**
- **Top-3 K05**: A ∩ B = {semua_perangkat, tidak_connect} (2 anggota), A ∪ B =
  {internet_mati_total, los_merah, pon_mati, router_tidak_punya_indikator,
  semua_perangkat, tidak_connect, wifi_tidak_muncul} (7 anggota) → 2 / 7 =
  **0.2857**

### S2 — Router tidak menyala setelah listrik padam

- **Top-1 K04**: A ∩ B = {power_mati, semua_perangkat, tidak_connect,
  wifi_tidak_muncul} (4 anggota), A ∪ B = {internet_mati, power_mati,
  semua_perangkat, tidak_connect, wifi_tidak_muncul} (5 anggota) → 4 / 5 =
  **0.8000**
- **Top-2 K05**: A ∩ B = {semua_perangkat, tidak_connect, wifi_tidak_muncul} (3
  anggota), A ∪ B = {power_mati, router_tidak_punya_indikator, semua_perangkat,
  tidak_connect, wifi_tidak_muncul} (5 anggota) → 3 / 5 = **0.6000**
- **Top-3 K01**: A ∩ B = {semua_perangkat, tidak_connect} (2 anggota), A ∪ B =
  {internet_mati, los_merah, pon_mati, power_mati, semua_perangkat,
  tidak_connect, wifi_tidak_muncul} (7 anggota) → 2 / 7 = **0.2857**

### S3 — Lampu PON normal tetapi tidak ada akses internet sama sekali

- **Top-1 K06**: A ∩ B = {connect_tapi_tanpa_internet, internet_mati,
  internet_mati_total, pon_nyala, semua_perangkat} (5 anggota), A ∪ B =
  {connect_tapi_tanpa_internet, internet_mati, internet_mati_total, los_mati,
  pon_nyala, semua_perangkat} (6 anggota) → 5 / 6 = **0.8333**
- **Top-2 K07**: A ∩ B = {connect_tapi_tanpa_internet, pon_nyala,
  semua_perangkat} (3 anggota), A ∪ B = {connect_tapi_tanpa_internet,
  internet_lambat, internet_mati, internet_mati_total, internet_nyala,
  pon_nyala, semua_perangkat} (7 anggota) → 3 / 7 = **0.4286**
- **Top-3 K01**: A ∩ B = {internet_mati, semua_perangkat} (2 anggota), A ∪ B =
  {connect_tapi_tanpa_internet, internet_mati, internet_mati_total, los_merah,
  pon_mati, pon_nyala, semua_perangkat, tidak_connect} (8 anggota) → 2 / 8 =
  **0.2500**

### S4 — Nama WiFi hilang karena lampu WLAN mati

- **Top-1 K08**: A ∩ B = {power_nyala, semua_perangkat, wifi_tidak_muncul,
  wlan_mati} (4 anggota), A ∪ B = {internet_nyala, power_nyala, semua_perangkat,
  wifi_tidak_muncul, wlan_mati} (5 anggota) → 4 / 5 = **0.8000**
- **Top-2 K09**: A ∩ B = {power_nyala, semua_perangkat, wlan_mati} (3 anggota),
  A ∪ B = {internet_nyala, pon_nyala, power_nyala, semua_perangkat,
  tidak_connect, wifi_tidak_muncul, wlan_mati} (7 anggota) → 3 / 7 = **0.4286**
- **Top-3 K05**: A ∩ B = {semua_perangkat, wifi_tidak_muncul} (2 anggota), A ∪ B
  = {power_nyala, router_tidak_punya_indikator, semua_perangkat, tidak_connect,
  wifi_tidak_muncul, wlan_mati} (6 anggota) → 2 / 6 = **0.3333**

### S5 — Password WiFi ditolak di semua perangkat setelah diganti

- **Top-1 K10**: A ∩ B = {password_ditolak, power_nyala, tidak_connect,
  wlan_nyala} (4 anggota), A ∪ B = {hanya_1_perangkat, password_ditolak,
  power_nyala, semua_perangkat, tidak_connect, wlan_nyala} (6 anggota) → 4 / 6 =
  **0.6667**
- **Top-2 K11**: A ∩ B = {password_ditolak, semua_perangkat, tidak_connect,
  wlan_nyala} (4 anggota), A ∪ B = {internet_nyala, password_ditolak,
  power_nyala, semua_perangkat, tidak_connect, wlan_nyala} (6 anggota) → 4 / 6 =
  **0.6667**
- **Top-3 K09**: A ∩ B = {power_nyala, semua_perangkat, tidak_connect} (3
  anggota), A ∪ B = {internet_nyala, password_ditolak, pon_nyala, power_nyala,
  semua_perangkat, tidak_connect, wlan_mati, wlan_nyala} (8 anggota) → 3 / 8 =
  **0.3750**

## 5. Catatan

- Leave-one-out menguji apakah kasus yang dikeluarkan kembali dikenali
  kategorinya dari 14 kasus lain. Cara ini mengukur konsistensi case base, bukan
  performa pada keluhan nyata.
- Lima skenario dibuat dari pola gejala yang mirip dengan kasus awal, sehingga
  akurasi yang tinggi belum tentu berlaku untuk keluhan yang sangat berbeda.
- Weighted Jaccard dapat mengubah urutan kandidat karena gejala lampu abnormal
  berbobot 2.0 dan gejala kondisi normal berbobot 0.5.
- Perhitungan rinci di bagian 4 memakai fungsi `core.similarity.hitung_rinci`
  yang sama dengan yang ditampilkan aplikasi, sehingga bisa dicocokkan dengan
  hitungan tangan di `docs/validasi_manual.md`.
