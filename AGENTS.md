# AGENTS.md

Panduan untuk AI coding agent (dan anggota tim) yang mengerjakan proyek ini.
Baca seluruh file ini sebelum menulis kode.

## Ringkasan Proyek

Sistem Pakar Troubleshooting WiFi rumah untuk mata kuliah **Kecerdasan Buatan**
(proyek kelompok). Metode: **Case-Based Reasoning (CBR) murni** dengan siklus
4R (Retrieve, Reuse, Revise, Retain), similarity **Jaccard**, antarmuka **Streamlit**.

Sistem mencocokkan keluhan baru (gejala + status lampu router) ke kasus lama yang
paling mirip, merekomendasikan solusinya, lalu belajar dari umpan balik pengguna.

## BATASAN WAJIB (pelanggaran = proyek ditolak dosen)

1. DILARANG Forward Chaining, Backward Chaining, dan rule-based IF-THEN sebagai mesin inferensi.
2. WAJIB CBR murni; fungsi `retrieve`, `reuse`, `revise`, `retain` terpisah dan eksplisit.
3. WAJIB Streamlit (bukan Flask/Django/console).
4. Basis pengetahuan = kumpulan **kasus**, bukan kumpulan aturan.
5. Status lampu router HANYA boleh menjadi atribut/gejala di dalam kasus.
   Contoh pelanggaran berat: `if status_los == "merah": kesimpulan = "kabel putus"`.
6. Parameter (`AMBANG_*`, `BOBOT_GEJALA`) adalah parameter similarity/retain, bukan aturan.
   Dilarang membuat percabangan yang memetakan gejala tertentu ke kesimpulan tertentu.
7. Dilarang: `rules = [...]`, `for rule in rules`, class `ForwardChaining`,
   `BackwardChaining`, `RuleEngine`, `InferenceEngine`, adaptasi solusi berbasis if-then.

Jika sebuah permintaan tampak mengharuskan melanggar batasan di atas, **berhenti dan tanyakan**,
jangan dikerjakan diam-diam.

## Struktur Proyek

```
app.py                      Entry point + router halaman (tanpa logika CBR)
core/
  case_base.py              Data & parameter: DAFTAR_GEJALA, PILIHAN_LAMPU, BOBOT_GEJALA,
                            ambang, CASE_BASE_AWAL (15 kasus)
  similarity.py             jaccard_similarity, weighted_jaccard_similarity, bandingkan_gejala,
                            hitung_rinci (untuk validasi manual)
  cbr_engine.py             retrieve, reuse, revise, retain
  storage.py                muat/simpan/reset case_base.json
ui/
  halaman_input.py          Halaman 1: input gejala
  halaman_hasil.py          Halaman 2: hasil diagnosis + feedback
  sidebar.py                Info metode, toggle similarity, daftar kasus, reset
  komponen.py               Komponen tampilan bersama
evaluasi/
  skenario_uji.py           5 skenario uji baru
  jalankan_evaluasi.py      Leave-one-out + uji skenario, Jaccard vs Weighted
tests/                      pytest (similarity + penjaga larangan rule-based)
docs/                       Catatan metodologi, hasil evaluasi, validasi manual
data/                       case_base.json (dibuat otomatis, di-gitignore)
```

Aturan dependensi: `core/` TIDAK boleh import Streamlit atau `ui/`. `ui/` boleh import `core/`.
`evaluasi/` dan `tests/` memakai `core/` saja.

## Konsep Penting

- **Gejala** = 25 boolean (Kelompok A keluhan, B lampu router, C info tambahan).
  Satu lampu = satu pilihan radio di UI, dikonversi ke satu gejala boolean.
  Opsi "Tidak tahu" tidak menghasilkan gejala.
- **Similarity** bekerja pada `set` nama gejala. Jaccard mengabaikan pasangan 0-0.
  Himpunan gabungan kosong menghasilkan 0.0.
- **Retrieve** melewati kasus berstatus `belum_terselesaikan`. Skor tertinggi di bawah
  `AMBANG_MIN_SIMILARITY` berarti "tidak ada kasus cukup mirip".
- **Reuse** menyalin solusi apa adanya + selisih gejala. Tanpa adaptasi if-then.
- **Revise** menangkap feedback; jika gagal tampilkan kandidat berikutnya; jika habis
  terima solusi baru dari pengguna.
- **Retain** menambah kasus baru, atau hanya menaikkan `jumlah_dipakai` jika duplikat
  (similarity >= `AMBANG_DUPLIKAT`). Selalu persist ke `data/case_base.json`.
- Struktur kasus: `id, nama_kasus, gejala, solusi, kategori_solusi, status, jumlah_dipakai, sumber`.

## Validasi Manual (Penting)

Dosen menguji dengan **menghitung similarity secara manual di papan tulis**, lalu
membandingkannya dengan output aplikasi. Karena itu:

- Similarity harus **bisa dihitung dengan tangan**: Jaccard `|A ∩ B| / |A ∪ B|`,
  Weighted Jaccard dengan bobot sederhana (0.5, 1.0, 2.0). Dilarang menambah rumus,
  normalisasi, atau pembulatan tersembunyi.
- Aplikasi wajib menampilkan **perhitungan rinci** (himpunan A, B, irisan, gabungan,
  pembilang, penyebut, hasil) lewat `similarity.hitung_rinci` dan expander di UI.
- Skor di tabel top-3 dan skor di perhitungan rinci harus berasal dari fungsi yang sama.
- Contoh hitungan tangan dicatat di `docs/validasi_manual.md` dan dipakai sebagai uji pytest.

## Konvensi Kode

- Komentar dan docstring dalam **Bahasa Indonesia**; nama variabel/fungsi **snake_case**.
- Docstring fungsi 4R menyebut nama tahap CBR-nya.
- Semua angka ambang dan bobot hanya ada di `core/case_base.py`, tidak di-hardcode di tempat lain.
- UI untuk demo sidang: tombol besar, pesan jelas, form dikelompokkan rapi.
- Streamlit: simpan state (hasil retrieve, indeks kandidat, status feedback) di `st.session_state`
  agar tombol tidak hilang saat rerun.
- Case base asli (`CASE_BASE_AWAL`) tidak boleh dimodifikasi saat runtime; selalu bekerja pada salinan.

## Perintah

```bash
pip install -r requirements.txt
streamlit run app.py                    # jalankan aplikasi
python -m pytest                        # jalankan uji (dari root proyek)
python -m evaluasi.jalankan_evaluasi    # evaluasi akurasi retrieval
```

## Definition of Done

- [ ] `streamlit run app.py` berjalan tanpa error dari awal.
- [ ] Empat fungsi 4R ada, terpisah, berdocstring.
- [ ] Skor similarity dan penjelasan gejala tampil di UI.
- [ ] Perhitungan rinci tampil di UI dan cocok dengan hitungan tangan.
- [ ] `docs/validasi_manual.md` terisi minimal 3 skenario hasil hitung tangan.
- [ ] Retain menambah jumlah kasus untuk kasus baru, dan hanya menaikkan counter untuk duplikat.
- [ ] Case base tetap ada setelah aplikasi di-restart (persistensi JSON).
- [ ] `tests/test_larangan_rule_based.py` lulus.
- [ ] Evaluasi dijalankan dan `docs/hasil_evaluasi.md` terisi.
- [ ] README dan `docs/catatan_metodologi.md` terisi (bukan sisa instruksi).

## Hal yang Tidak Boleh Dilakukan Agent

- Menambah framework UI lain atau mengganti Streamlit.
- Mengubah batasan di dokumen ini tanpa persetujuan tim.
- Menulis solusi kasus berupa placeholder ("isi nanti", "lorem ipsum").
- Menambah dependensi tanpa alasan jelas; catat di `requirements.txt` bila memang perlu.
