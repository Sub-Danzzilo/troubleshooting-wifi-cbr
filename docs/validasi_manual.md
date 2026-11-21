# Validasi Manual (Hitungan Papan Tulis)

Dokumen ini berisi perhitungan similarity yang dikerjakan **dengan tangan**, lalu dicocokkan
dengan output aplikasi. Dipakai untuk latihan sidang dan sebagai dasar uji pytest.

> Instruksi: isi bagian "Skenario" dengan kasus nyata dari case base kalian setelah
> `CASE_BASE_AWAL` selesai. Hitung dulu dengan tangan, baru bandingkan dengan aplikasi.
> Jangan menyalin angka dari output program.

## Rumus

**Jaccard:** `similarity = |A ∩ B| / |A ∪ B|`

**Weighted Jaccard:** `similarity = Σ bobot (A ∩ B) / Σ bobot (A ∪ B)`

A = gejala input pengguna, B = gejala pada kasus di case base.

## Contoh Format (angka ilustrasi, ganti dengan data asli)

Input A = {`tidak_connect`, `semua_perangkat`, `los_merah`}
Kasus B = {`tidak_connect`, `semua_perangkat`, `los_merah`, `pon_mati`}

| Langkah | Hasil |
|---|---|
| A ∩ B | {`tidak_connect`, `semua_perangkat`, `los_merah`} → 3 anggota |
| A ∪ B | {`tidak_connect`, `semua_perangkat`, `los_merah`, `pon_mati`} → 4 anggota |
| Jaccard | 3 / 4 = **0,75** |

Weighted (bobot: `los_merah` 2,0 · `pon_mati` 2,0 · lainnya 1,0):

| Langkah | Hasil |
|---|---|
| Σ bobot irisan | 1 + 1 + 2 = 4 |
| Σ bobot gabungan | 1 + 1 + 2 + 2 = 6 |
| Weighted Jaccard | 4 / 6 ≈ **0,667** |

## Skenario 1 (TODO)

- Deskripsi keluhan:
- Himpunan A:
- Tabel hitungan per kasus (minimal top-3): irisan, gabungan, pembilang, penyebut, hasil
- Kasus terpilih (manual):
- Output aplikasi:
- Cocok? (Ya/Tidak, jika tidak: catat penyebabnya)

## Skenario 2 (TODO)

(format sama seperti Skenario 1)

## Skenario 3 (TODO)

(format sama seperti Skenario 1)

## Latihan Sidang

- [ ] Setiap anggota bisa menghitung Jaccard satu pasang kasus tanpa melihat catatan.
- [ ] Bisa menjelaskan kenapa gejala yang tidak dipilih tidak ikut dihitung (pasangan 0-0).
- [ ] Bisa menunjukkan di aplikasi bagian "perhitungan rinci" dan mencocokkannya dengan papan tulis.
- [ ] Tabel ringkas 15 kasus (ID + gejala) sudah disiapkan sebagai contekan.
