# Catatan Metodologi (bahan laporan)

Dokumen ini merangkum alasan pemilihan metode dan representasi yang dipakai sistem.
Bahan ini bisa langsung dikembangkan menjadi bab metode di laporan.

## 1. Mengapa CBR, bukan rule-based

Pengetahuan troubleshooting WiFi di lapangan berbentuk **pengalaman kasus**: seorang
teknisi mengingat kombinasi gejala yang pernah dia temui beserta langkah yang berhasil.
Pengetahuan itu tidak rapi seperti aturan IF-THEN, dan sering ada pengecualian yang sulit
dirumuskan di awal.

CBR cocok karena:

- Pakar tidak perlu merumuskan seluruh aturan sebelum sistem bisa dipakai; cukup
  mengumpulkan kasus nyata.
- Sistem dapat **belajar** dari pengalaman baru lewat tahap Retain.
- Keputusan bisa dipertanggungjawabkan: ada kasus rujukan, skor kemiripan, dan daftar
  gejala yang cocok/tidak cocok.
- Status lampu router diperlakukan sebagai **atribut kasus**, bukan pemicu kesimpulan.
  Tidak ada aturan seperti "LOS merah berarti kabel putus"; makna lampu melekat pada
  kasus-kasus yang memuatnya.

Sistem ini tidak memakai Forward Chaining, Backward Chaining, maupun mesin aturan.
`tests/test_larangan_rule_based.py` memindai `core/`, `ui/`, dan `app.py` untuk memastikan
tidak ada identifier atau pola rule-based yang masuk.

## 2. Representasi kasus

Satu kasus berisi:

| Field | Isi |
|---|---|
| `id` | K01, K02, ... (otomatis K16 dan seterusnya untuk kasus hasil retain) |
| `nama_kasus` | Ringkasan satu baris |
| `gejala` | Daftar nama gejala boolean (4-6 gejala per kasus awal) |
| `solusi` | Langkah perbaikan yang konkret dan berurutan |
| `kategori_solusi` | Kelompok penyebab, dipakai untuk evaluasi |
| `status` | `berhasil` atau `belum_terselesaikan` |
| `jumlah_dipakai` | Berapa kali kasus ini dipakai/dikonfirmasi berhasil |
| `sumber` | `awal` atau `retain` |

Gejala ada 25 dan dikelompokkan menjadi tiga: keluhan utama (7), status lampu router (15),
dan informasi tambahan (3). Setiap lampu (POWER, PON, LOS, INTERNET, WLAN, LAN) dipecah
menjadi beberapa gejala yang saling eksklusif, misalnya `los_mati`, `los_merah`, dan
`los_kedip`. Cara ini disebut representasi one-hot.

Alasannya sederhana: similarity Jaccard bekerja pada himpunan, sehingga setiap pilihan
lampu harus menjadi anggota himpunan yang berbeda. Opsi "Tidak tahu" tidak menghasilkan
gejala apa pun, yang berarti pengguna tidak melaporkan status lampu tersebut.

Lampu tetap hanya atribut: tidak ada kode yang membaca `los_merah` lalu menyimpulkan
sesuatu. Kode hanya menghitung seberapa banyak gejala input beririsan dengan gejala kasus.

## 3. Pemilihan Jaccard dan Weighted Jaccard

**Jaccard** dipilih karena paling mudah dihitung manual:

`similarity = |A ∩ B| / |A ∪ B|`

Contoh: input A punya 5 gejala, kasus B punya 5 gejala, 4 di antaranya sama.
Maka `4 / (5 + 5 - 4) = 4/6 = 0,6667`.

**Weighted Jaccard** memakai rumus yang sama, tetapi setiap gejala punya bobot:

`similarity = Σ bobot(A ∩ B) / Σ bobot(A ∪ B)`

Bobot hanya memakai tiga nilai sederhana: 0,5; 1,0; dan 2,0.

| Kelompok gejala | Bobot | Alasan |
|---|---|---|
| Keluhan utama dan informasi tambahan | 1,0 | Pembeda umum, tidak terlalu menonjol |
| Lampu kondisi normal (`power_nyala`, `pon_nyala`, `los_mati`, `internet_nyala`, `wlan_nyala`, `lan_nyala`) | 0,5 | Muncul di banyak kasus, kurang membedakan |
| Lampu menyimpang (`power_mati`, `los_merah`, `los_kedip`, `pon_mati`, `internet_mati`, `wlan_mati`, `lan_mati`) | 2,0 | Menunjukkan gangguan spesifik, layak lebih dipertimbangkan |

Bobot adalah **parameter similarity**, bukan aturan inferensi. Mengubah bobot hanya
mengubah urutan kemiripan, bukan menambah kesimpulan baru.

Perbandingan keduanya dibahas di `docs/hasil_evaluasi.md`. Pada kasus yang gejalanya
seri di Jaccard, Weighted Jaccard kadang membedakan kandidat karena gejala lampu abnormal
berbobot lebih tinggi (contoh: K10 vs K11 pada `docs/validasi_manual.md`).

## 4. Gejala tidak dipilih = tidak dilaporkan

Jaccard hanya melihat gejala yang **ada** di himpunan. Pasangan gejala yang sama-sama
False (0-0) tidak menambah irisan maupun gabungan, sehingga diabaikan.

Kelebihan:

- Perhitungan mudah dan transparan.
- Pengguna tidak perlu menjawab semua 25 gejala; cukup yang diketahui.
- Opsi "Tidak tahu" pada lampu tidak merusak skor karena tidak menghasilkan gejala.

Kekurangan:

- Dua kasus yang sama-sama tidak memiliki suatu gejala tidak dianggap mirip karena hal itu.
- Kasus dengan banyak gejala bisa terlihat kurang mirip hanya karena gejalanya lebih lengkap.
- Informasi "gejala ini sudah dicek dan hasilnya normal" tidak terepresentasi, kecuali
  gejala kondisi normal seperti `los_mati` ikut dipilih.

Karena itu Weighted Jaccard memberi bobot kecil pada gejala kondisi normal agar
kecocokan pada kondisi normal tidak mendominasi.

## 5. Keterbatasan

- **Cakupan case base kecil.** Lima belas kasus awal belum mewakili semua gangguan WiFi
  rumah. Kasus di luar pola tersebut bisa mendapat skor di bawah ambang.
- **Sensitivitas bobot.** Perubahan bobot dapat mengubah kandidat top-1, terutama bila
  skor beberapa kasus berdekatan.
- **One-hot kaku.** Dua pilihan lampu yang mirip maknanya (misalnya `los_kedip` dan
  `los_merah`) dianggap sama sekali berbeda oleh Jaccard.
- **Ambang tetap.** `AMBANG_MIN_SIMILARITY = 0.30` dan `AMBANG_DUPLIKAT = 1.0` ditentukan
  manual; belum dioptimasi dari data.
- **Kualitas solusi bergantung pada kasus rujukan.** Reuse menyalin solusi apa adanya,
  tanpa adaptasi, sehingga solusi hanya sebaik kasus yang paling mirip.
- **Evaluasi terbatas.** Leave-one-out dan lima skenario baru mengukur konsistensi case base,
  bukan performa pada keluhan nyata dalam jumlah besar.
