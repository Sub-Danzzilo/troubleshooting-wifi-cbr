# AGENTS.md

Panduan untuk AI coding agent (dan anggota tim) yang mengerjakan proyek ini.
Baca seluruh file ini sebelum menulis kode.

## Ringkasan Proyek

Sistem Pakar Troubleshooting WiFi rumah untuk mata kuliah **Kecerdasan Buatan**
(proyek kelompok). Metode: **Case-Based Reasoning (CBR) murni** dengan siklus 4R
(Retrieve, Reuse, Revise, Retain), similarity **Jaccard**, antarmuka
**Streamlit**.

Sistem mencocokkan keluhan baru (gejala + status lampu router) ke kasus lama
yang paling mirip, merekomendasikan solusinya, lalu belajar dari umpan balik
pengguna.

## BATASAN WAJIB (pelanggaran = proyek ditolak dosen)

1. DILARANG Forward Chaining, Backward Chaining, dan rule-based IF-THEN sebagai
   mesin inferensi.
2. WAJIB CBR murni; fungsi `retrieve`, `reuse`, `revise`, `retain` terpisah dan
   eksplisit.
3. WAJIB Streamlit (bukan Flask/Django/console).
4. Basis pengetahuan = kumpulan **kasus**, bukan kumpulan aturan.
5. Status lampu router HANYA boleh menjadi atribut/gejala di dalam kasus. Contoh
   pelanggaran berat: `if status_los == "merah": kesimpulan = "kabel putus"`.
6. Parameter (`AMBANG_*`, `BOBOT_GEJALA`) adalah parameter similarity/retain,
   bukan aturan. Dilarang membuat percabangan yang memetakan gejala tertentu ke
   kesimpulan tertentu.
7. Dilarang: `rules = [...]`, `for rule in rules`, class `ForwardChaining`,
   `BackwardChaining`, `RuleEngine`, `InferenceEngine`, adaptasi solusi berbasis
   if-then.

Jika sebuah permintaan tampak mengharuskan melanggar batasan di atas, **berhenti
dan tanyakan**, jangan dikerjakan diam-diam.

## Struktur Proyek

```text
app.py                      Entry point + router halaman (tanpa logika CBR)
pyproject.toml              Konfigurasi mypy dan Pyright/Pylance
.markdownlint.json          Aturan markdownlint proyek
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
tests/                      pytest (similarity, siklus 4R, penjaga larangan rule-based)
docs/                       Metodologi, evaluasi, validasi & panduan manual
data/                       case_base.json (dibuat otomatis, di-gitignore)
```

Aturan dependensi: `core/` TIDAK boleh import Streamlit atau `ui/`. `ui/` boleh
import `core/`. `evaluasi/` dan `tests/` memakai `core/` saja.

## Konsep Penting

- **Gejala** = 25 boolean (Kelompok A keluhan, B lampu router, C info tambahan).
  Satu lampu = satu pilihan radio di UI, dikonversi ke satu gejala boolean. Opsi
  "Tidak tahu" tidak menghasilkan gejala.
- **Similarity** bekerja pada `set` nama gejala. Jaccard mengabaikan pasangan
  0-0. Himpunan gabungan kosong menghasilkan 0.0.
- **Retrieve** melewati kasus berstatus `belum_terselesaikan`. Skor tertinggi di
  bawah `AMBANG_MIN_SIMILARITY` berarti "tidak ada kasus cukup mirip".
- **Reuse** menyalin solusi apa adanya + selisih gejala. Tanpa adaptasi if-then.
- **Revise** menangkap feedback; jika gagal tampilkan kandidat berikutnya; jika
  habis terima solusi baru dari pengguna.
- **Retain** menambah kasus baru, atau hanya menaikkan `jumlah_dipakai` jika
  duplikat (similarity >= `AMBANG_DUPLIKAT`). Selalu persist ke
  `data/case_base.json`.
- Struktur kasus:
  `id, nama_kasus, gejala, solusi, kategori_solusi, status, jumlah_dipakai, sumber`.

## Validasi Manual (Penting)

Dosen menguji dengan **menghitung similarity secara manual di papan tulis**,
lalu membandingkannya dengan output aplikasi. Karena itu:

- Similarity harus **bisa dihitung dengan tangan**: Jaccard `|A ∩ B| / |A ∪ B|`,
  Weighted Jaccard dengan bobot sederhana (0.5, 1.0, 2.0). Dilarang menambah
  rumus, normalisasi, atau pembulatan tersembunyi.
- Aplikasi wajib menampilkan **perhitungan rinci** (himpunan A, B, irisan,
  gabungan, pembilang, penyebut, hasil) lewat `similarity.hitung_rinci` dan
  expander di UI.
- Skor di tabel top-3 dan skor di perhitungan rinci harus berasal dari fungsi
  yang sama.
- Contoh hitungan tangan dicatat di `docs/validasi_manual.md` dan dipakai
  sebagai uji pytest.

## Konvensi Kode

- Komentar dan docstring dalam **Bahasa Indonesia**; nama variabel/fungsi
  **snake_case**.
- Docstring fungsi 4R menyebut nama tahap CBR-nya.
- Semua angka ambang dan bobot hanya ada di `core/case_base.py`, tidak
  di-hardcode di tempat lain.
- UI untuk demo sidang: tombol besar, pesan jelas, form dikelompokkan rapi.
- Streamlit: simpan state (hasil retrieve, indeks kandidat, status feedback) di
  `st.session_state` agar tombol tidak hilang saat rerun.
- Case base asli (`CASE_BASE_AWAL`) tidak boleh dimodifikasi saat runtime;
  selalu bekerja pada salinan.

## Pemeriksaan Tipe (wajib)

- Semua fungsi, termasuk helper internal dan fungsi uji, wajib punya type hint
  lengkap.
- Konfigurasi ada di `pyproject.toml`: bagian `[tool.mypy]` untuk mypy dan
  `[tool.pyright]` untuk Pyright (Pylance di VS Code membaca konfigurasi yang
  sama).
- Setelah menulis atau mengubah kode Python, jalankan salah satu (keduanya lebih
  baik):

  ```bash
  python -m mypy
  python -m pyright
  ```

- Pekerjaan belum dianggap selesai bila masih ada error tipe. Jangan
  menonaktifkan pemeriksaan, menurunkan mode Pyright, atau menambah
  `# type: ignore` tanpa alasan hanya agar pemeriksaan lulus.
- Bila `# type: ignore[...]` benar-benar diperlukan (misalnya keterbatasan stub
  pihak ketiga), tulis kode error yang spesifik dan jelaskan alasannya di
  komentar.

## Pemeriksaan Markdown (wajib)

- Setiap kali menulis atau mengubah berkas `.md`, jalankan markdownlint
  **sebelum** pekerjaan dianggap selesai.
- Target harus disebutkan secara spesifik: hanya berkas yang diubah, atau
  seluruh berkas markdown proyek.

  ```bash
  # hanya berkas yang diubah
  npx --yes markdownlint-cli2 docs/panduan_pengujian_manual.md

  # seluruh berkas markdown proyek
  npx --yes markdownlint-cli2 README.md AGENTS.md \
    "docs/*.md" "catatan-laporan/*.md"
  ```

  Bila `npx` tidak tersedia, ganti dengan `bunx markdownlint-cli2` dan target
  yang sama.
- Jangan memakai pola `**/*.md` tanpa pengecualian karena ikut memindai
  `.venv/` dan `node_modules/`.
- Patokan lulus: **0 warning**. Konfigurasi proyek ada di `.markdownlint.json`
  (batas 80 karakter; baris tabel dikecualikan karena isi sel tidak bisa
  dibungkus).
- Urutan perbaikan yang dianjurkan: benahi isinya dulu (bungkus teks ke 80
  kolom, seragamkan gaya tabel, beri bahasa pada blok kode), jangan langsung
  mematikan aturan.
- Bila memang tidak ada jalan lain (contoh: tabel panjang yang tidak mungkin
  dipecah tanpa merusak isi), warning boleh diabaikan. Pilih salah satu:
  1. longgarkan aturan di `.markdownlint.json` dan tulis alasannya, atau
  2. tandai baris terkait dengan `<!-- markdownlint-disable-line MD0xx -->`
     disertai alasan.

  Jangan mematikan seluruh berkas dengan `<!-- markdownlint-disable -->`
  tanpa penjelasan.

## Perintah

```bash
pip install -r requirements.txt
streamlit run app.py                    # jalankan aplikasi
python -m pytest                        # jalankan uji (dari root proyek)
python -m mypy                          # cek tipe dengan mypy (wajib)
python -m pyright                       # alternatif cek tipe, konfigurasi sama
python -m evaluasi.jalankan_evaluasi    # evaluasi akurasi retrieval

# cek markdown (wajib setelah menulis/mengubah berkas .md)
npx --yes markdownlint-cli2 README.md AGENTS.md \
  "docs/*.md" "catatan-laporan/*.md"
```

## Commit dan Push

- Setiap balasan yang menambah, mengubah, atau menghapus berkas WAJIB
  diakhiri usulan **commit message dalam Bahasa Inggris** (bukan dijalankan
  sendiri), beserta daftar berkas yang masuk commit tersebut.
- Format yang dipakai: Conventional Commits, judul singkat satu baris, lalu body
  secukupnya bila perubahan perlu dijelaskan.
- Agent TIDAK boleh menjalankan `git commit`, `git push`, atau mengubah
  konfigurasi git. Commit dan push sepenuhnya tanggung jawab anggota tim.
- Bila perubahan sebaiknya dipecah, usulkan beberapa commit message terpisah dan
  sebutkan berkas yang masuk ke masing-masing commit.

## Definition of Done

- [ ] `streamlit run app.py` berjalan tanpa error dari awal.
- [ ] `python -m mypy` dan/atau `python -m pyright` lulus tanpa error tipe.
- [ ] Empat fungsi 4R ada, terpisah, berdocstring.
- [ ] Skor similarity dan penjelasan gejala tampil di UI.
- [ ] Perhitungan rinci tampil di UI dan cocok dengan hitungan tangan.
- [ ] `docs/validasi_manual.md` terisi minimal 3 skenario hasil hitung tangan.
- [ ] Retain menambah jumlah kasus untuk kasus baru, dan hanya menaikkan counter
  untuk duplikat.
- [ ] Case base tetap ada setelah aplikasi di-restart (persistensi JSON).
- [ ] `tests/test_larangan_rule_based.py` lulus.
- [ ] Evaluasi dijalankan dan `docs/hasil_evaluasi.md` terisi.
- [ ] README dan `docs/catatan_metodologi.md` terisi (bukan sisa instruksi).
- [ ] `markdownlint` bersih (0 warning) untuk setiap berkas `.md` yang diubah.
- [ ] Usulan commit message beserta daftar berkas disertakan di akhir balasan.

## Hal yang Tidak Boleh Dilakukan Agent

- Menambah framework UI lain atau mengganti Streamlit.
- Mengubah batasan di dokumen ini tanpa persetujuan tim.
- Menulis solusi kasus berupa placeholder ("isi nanti", "lorem ipsum").
- Menambah dependensi tanpa alasan jelas; catat di `requirements.txt` bila
  memang perlu.
- Mematikan atau melunakkan pemeriksaan tipe (mypy/Pyright) hanya agar kode
  dianggap lulus.
- Mematikan aturan markdownlint untuk seluruh berkas tanpa alasan yang jelas.
