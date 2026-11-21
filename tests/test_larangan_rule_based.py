# =============================================================================
# tests/test_larangan_rule_based.py  —  PENJAGA BATASAN DOSEN
# =============================================================================
# ISI FILE INI NANTINYA:
#   - Uji otomatis yang memindai seluruh file .py di core/, ui/, dan app.py
#     (kecuali folder tests/) dan GAGAL jika menemukan pola terlarang:
#       * nama class/identifier: ForwardChaining, BackwardChaining, RuleEngine, InferenceEngine
#       * variabel/struktur bernama "rules"
#       * pola "if" yang membandingkan variabel lampu/gejala dengan string
#         kesimpulan (mis. membandingkan status lampu dengan "merah")
#   - Uji ini mendukung Kriteria Evaluasi #6 (bukti bahwa lampu hanya atribut kasus).
#   - Tambahkan juga uji bahwa fungsi retrieve, reuse, revise, retain semuanya ada
#     di core.cbr_engine (Kriteria #1).
