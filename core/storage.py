# =============================================================================
# core/storage.py  —  PERSISTENSI CASE BASE (JSON)
# =============================================================================
# ISI FILE INI NANTINYA:
#
# 1. muat_case_base() -> list
#    - Baca data/case_base.json (encoding UTF-8).
#    - Jika file tidak ada ATAU rusak: buat ulang dari CASE_BASE_AWAL dan tulis ke disk.
#
# 2. simpan_case_base(case_base) -> None
#    - Tulis ke JSON dengan indent dan ensure_ascii=False (agar teks Indonesia terbaca).
#    - Dipanggil setiap kali retain mengubah case base.
#
# 3. reset_case_base() -> list
#    - Timpa JSON dengan salinan CASE_BASE_AWAL, kembalikan salinan itu.
#    - Gunakan salinan (copy) agar CASE_BASE_AWAL tidak ikut berubah.
#
# CATATAN: pastikan folder data/ ada sebelum menulis.
