# =============================================================================
# tests/test_similarity.py  —  UJI UNIT SIMILARITY (pytest)
# =============================================================================
# ISI FILE INI NANTINYA:
#   - Kasus identik -> similarity 1.0.
#   - Tidak ada irisan -> similarity 0.0.
#   - Dua himpunan kosong -> 0.0 (tidak error bagi nol).
#   - Contoh hitung manual (irisan 2, gabungan 4 -> 0.5).
#   - Weighted Jaccard dengan bobot 1.0 semua harus sama dengan Jaccard biasa.
#   - Gejala bobot tinggi di irisan menaikkan skor dibanding bobot rendah.
#   - Cocokkan hasil fungsi dengan contoh hitungan tangan di docs/validasi_manual.md
#     (setiap contoh di dokumen itu = satu uji; nilai harapan ditulis dari hitungan manual,
#     BUKAN disalin dari output program).
#   - hitung_rinci: pembilang/penyebut yang dikembalikan sesuai hitungan manual,
#     dan hasilnya sama dengan jaccard_similarity.