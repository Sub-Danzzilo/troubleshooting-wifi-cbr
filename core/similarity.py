"""Perhitungan kemiripan (similarity) antara himpunan gejala.

Semua fungsi murni: hanya menerima input dan mengembalikan hasil, tanpa membaca
file, tanpa Streamlit, dan tanpa efek samping.

Catatan penting untuk validasi manual: pasangan gejala yang sama-sama False
(0-0) tidak masuk perhitungan karena representasi yang dipakai adalah himpunan
nama gejala. "Gejala tidak dipilih" berarti "tidak dilaporkan", bukan cocok.
"""

from core.case_base import BOBOT_GEJALA, LABEL_GEJALA


def _sebagai_set(gejala):
    """Ubah list/tuple/set nama gejala menjadi set (None dianggap kosong)."""
    return set(gejala or [])


def jaccard_similarity(himpunan_a, himpunan_b):
    """Similarity Jaccard: |A ∩ B| / |A ∪ B|.

    Parameter:
        himpunan_a, himpunan_b: kumpulan nama gejala (list/set).
    Mengembalikan 0.0 bila gabungan kosong (menghindari pembagian nol).
    """
    a = _sebagai_set(himpunan_a)
    b = _sebagai_set(himpunan_b)
    gabungan = a | b
    if not gabungan:
        return 0.0
    return len(a & b) / len(gabungan)


def weighted_jaccard_similarity(himpunan_a, himpunan_b, bobot=None):
    """Weighted Jaccard: Σ bobot(A ∩ B) / Σ bobot(A ∪ B).

    Parameter:
        himpunan_a, himpunan_b: kumpulan nama gejala.
        bobot: dict {nama_gejala: bobot}. Gejala yang tidak ada di dict
               dianggap berbobot 1.0. Default memakai BOBOT_GEJALA.
    Mengembalikan 0.0 bila gabungan kosong.
    """
    if bobot is None:
        bobot = BOBOT_GEJALA
    a = _sebagai_set(himpunan_a)
    b = _sebagai_set(himpunan_b)
    gabungan = a | b
    if not gabungan:
        return 0.0

    def bobot_gejala(nama):
        return float(bobot.get(nama, 1.0))

    jumlah_irisan = sum(bobot_gejala(nama) for nama in a & b)
    jumlah_gabungan = sum(bobot_gejala(nama) for nama in gabungan)
    return jumlah_irisan / jumlah_gabungan


def bandingkan_gejala(gejala_input, gejala_kasus):
    """Bandingkan dua himpunan gejala untuk penjelasan transparan.

    Mengembalikan dict berisi tiga kelompok (diurutkan alfabetis):
        cocok       : gejala di A ∩ B
        hanya_input : gejala yang hanya dilaporkan pengguna
        hanya_kasus : gejala yang hanya ada pada kasus
    """
    a = _sebagai_set(gejala_input)
    b = _sebagai_set(gejala_kasus)
    return {
        "cocok": sorted(a & b),
        "hanya_input": sorted(a - b),
        "hanya_kasus": sorted(b - a),
    }


def hitung_rinci(gejala_input, gejala_kasus, mode="jaccard", bobot=None):
    """Kembalikan seluruh langkah perhitungan untuk validasi manual.

    Parameter:
        gejala_input, gejala_kasus: kumpulan nama gejala.
        mode: "jaccard" atau "weighted".
        bobot: dict bobot (hanya dipakai pada mode weighted).

    Hasil["hasil"] dihitung memakai fungsi similarity yang sama dengan yang
    dipakai retrieve, jadi angka pada tabel top-3 dan perhitungan rinci selalu
    identik.
    """
    if mode not in ("jaccard", "weighted"):
        raise ValueError("Mode similarity harus 'jaccard' atau 'weighted'.")
    if bobot is None:
        bobot = BOBOT_GEJALA

    a = _sebagai_set(gejala_input)
    b = _sebagai_set(gejala_kasus)
    irisan = a & b
    gabungan = a | b

    rinci = {
        "mode": mode,
        "himpunan_a": sorted(a),
        "himpunan_b": sorted(b),
        "irisan": sorted(irisan),
        "gabungan": sorted(gabungan),
        "jumlah_a": len(a),
        "jumlah_b": len(b),
        "jumlah_irisan": len(irisan),
        "jumlah_gabungan": len(gabungan),
        "bobot_irisan": [],
        "bobot_gabungan": [],
        "jumlah_bobot_irisan": 0.0,
        "jumlah_bobot_gabungan": 0.0,
    }

    if mode == "jaccard":
        rinci["pembilang"] = len(irisan)
        rinci["penyebut"] = len(gabungan)
        rinci["hasil"] = jaccard_similarity(a, b)
        rinci["rumus"] = "|A ∩ B| / |A ∪ B|"
    else:
        def bobot_gejala(nama):
            return float(bobot.get(nama, 1.0))

        rinci["bobot_irisan"] = [
            {"gejala": nama, "label": LABEL_GEJALA.get(nama, nama), "bobot": bobot_gejala(nama)}
            for nama in sorted(irisan)
        ]
        rinci["bobot_gabungan"] = [
            {"gejala": nama, "label": LABEL_GEJALA.get(nama, nama), "bobot": bobot_gejala(nama)}
            for nama in sorted(gabungan)
        ]
        rinci["jumlah_bobot_irisan"] = sum(item["bobot"] for item in rinci["bobot_irisan"])
        rinci["jumlah_bobot_gabungan"] = sum(item["bobot"] for item in rinci["bobot_gabungan"])
        rinci["pembilang"] = rinci["jumlah_bobot_irisan"]
        rinci["penyebut"] = rinci["jumlah_bobot_gabungan"]
        rinci["hasil"] = weighted_jaccard_similarity(a, b, bobot)
        rinci["rumus"] = "Σ bobot(A ∩ B) / Σ bobot(A ∪ B)"

    return rinci
