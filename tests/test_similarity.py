"""Uji unit similarity, termasuk contoh hitung tangan di docs/validasi_manual.md.

Nilai harapan ditulis dari hitungan manual (pecahan), bukan dari output program.
"""

import pytest

from core.case_base import BOBOT_GEJALA, CASE_BASE_AWAL
from core.similarity import (
    bandingkan_gejala,
    hitung_rinci,
    jaccard_similarity,
    weighted_jaccard_similarity,
)


def gejala_kasus(kasus_id: str) -> list[str]:
    kasus = next(kasus for kasus in CASE_BASE_AWAL if kasus["id"] == kasus_id)
    return kasus["gejala"]


# --- Skenario 1 di docs/validasi_manual.md --------------------------------
INPUT_FIBER: list[str] = [
    "tidak_connect",
    "semua_perangkat",
    "internet_mati_total",
    "los_merah",
    "pon_mati",
]

# --- Skenario 2 di docs/validasi_manual.md --------------------------------
INPUT_PASSWORD: list[str] = [
    "tidak_connect",
    "password_ditolak",
    "semua_perangkat",
    "wlan_nyala",
    "power_nyala",
]

# --- Skenario 3 di docs/validasi_manual.md --------------------------------
INPUT_SINYAL: list[str] = [
    "internet_lambat",
    "sinyal_lemah",
    "hanya_1_perangkat",
    "wlan_nyala",
]


def test_himpunan_identik_bernilai_satu() -> None:
    assert jaccard_similarity({"a", "b"}, ["b", "a"]) == 1.0


def test_tidak_ada_irisan_bernilai_nol() -> None:
    assert jaccard_similarity({"a", "b"}, {"c", "d"}) == 0.0


def test_dua_himpunan_kosong_bernilai_nol() -> None:
    assert jaccard_similarity(set(), set()) == 0.0
    assert weighted_jaccard_similarity([], []) == 0.0


def test_contoh_manual_irisan_dua_gabungan_empat() -> None:
    # |A ∩ B| = 2, |A ∪ B| = 4
    assert jaccard_similarity({"a", "b", "c"}, {"a", "b", "d"}) == pytest.approx(0.5)


def test_weighted_sama_dengan_jaccard_bila_semua_bobot_satu() -> None:
    bobot = {"a": 1.0, "b": 1.0, "c": 1.0, "d": 1.0}
    a, b = {"a", "b", "c"}, {"a", "b", "d"}
    assert weighted_jaccard_similarity(a, b, bobot) == pytest.approx(jaccard_similarity(a, b))


def test_bobot_tinggi_di_irisan_menaikkan_skor() -> None:
    a = {"gejala_umum", "gejala_penting"}
    b = {"gejala_umum", "gejala_penting", "gejala_lain"}
    bobot_rendah = {"gejala_umum": 1.0, "gejala_penting": 0.5, "gejala_lain": 2.0}
    bobot_tinggi = {"gejala_umum": 1.0, "gejala_penting": 2.0, "gejala_lain": 0.5}
    assert weighted_jaccard_similarity(a, b, bobot_tinggi) > weighted_jaccard_similarity(
        a, b, bobot_rendah
    )


def test_skenario_1_jaccard_dan_weighted() -> None:
    kasus = gejala_kasus("K01")
    # A ∩ B = 4, A ∪ B = 6
    assert jaccard_similarity(INPUT_FIBER, kasus) == pytest.approx(4 / 6)
    # Σ bobot irisan = 6, Σ bobot gabungan = 9
    assert weighted_jaccard_similarity(INPUT_FIBER, kasus, BOBOT_GEJALA) == pytest.approx(6 / 9)


def test_skenario_1_kasus_pembanding() -> None:
    kasus_k02 = gejala_kasus("K02")
    kasus_k04 = gejala_kasus("K04")
    kasus_k06 = gejala_kasus("K06")

    # K02: A ∩ B = 3, A ∪ B = 8; Σ bobot irisan 4, Σ bobot gabungan 9,5
    assert jaccard_similarity(INPUT_FIBER, kasus_k02) == pytest.approx(3 / 8)
    assert weighted_jaccard_similarity(INPUT_FIBER, kasus_k02, BOBOT_GEJALA) == pytest.approx(4 / 9.5)

    # K04: A ∩ B = 2, A ∪ B = 8; Σ bobot irisan 2, Σ bobot gabungan 12
    assert jaccard_similarity(INPUT_FIBER, kasus_k04) == pytest.approx(2 / 8)
    assert weighted_jaccard_similarity(INPUT_FIBER, kasus_k04, BOBOT_GEJALA) == pytest.approx(2 / 12)

    # K06: A ∩ B = 2, A ∪ B = 9; Σ bobot irisan 2, Σ bobot gabungan 11
    assert jaccard_similarity(INPUT_FIBER, kasus_k06) == pytest.approx(2 / 9)
    assert weighted_jaccard_similarity(INPUT_FIBER, kasus_k06, BOBOT_GEJALA) == pytest.approx(2 / 11)


def test_skenario_2_jaccard_seri_dan_weighted() -> None:
    kasus_k10 = gejala_kasus("K10")
    kasus_k11 = gejala_kasus("K11")
    # Jaccard sama-sama 4/6 (seri), Weighted membedakan K11 (3,5 / 4,5)
    assert jaccard_similarity(INPUT_PASSWORD, kasus_k10) == pytest.approx(4 / 6)
    assert jaccard_similarity(INPUT_PASSWORD, kasus_k11) == pytest.approx(4 / 6)
    assert weighted_jaccard_similarity(INPUT_PASSWORD, kasus_k10, BOBOT_GEJALA) == pytest.approx(3 / 5)
    assert weighted_jaccard_similarity(INPUT_PASSWORD, kasus_k11, BOBOT_GEJALA) == pytest.approx(3.5 / 4.5)


def test_skenario_3_jaccard_dan_weighted() -> None:
    kasus_k14 = gejala_kasus("K14")
    # A ∩ B = 3, A ∪ B = 5
    assert jaccard_similarity(INPUT_SINYAL, kasus_k14) == pytest.approx(3 / 5)
    # Σ bobot irisan = 2,5, Σ bobot gabungan = 4,5
    assert weighted_jaccard_similarity(INPUT_SINYAL, kasus_k14, BOBOT_GEJALA) == pytest.approx(2.5 / 4.5)


def test_bandingkan_gejala_mengelompokkan_tiga_bagian() -> None:
    hasil = bandingkan_gejala({"a", "b"}, {"b", "c"})
    assert hasil == {"cocok": ["b"], "hanya_input": ["a"], "hanya_kasus": ["c"]}


def test_hitung_rinci_jaccard_konsisten_dengan_fungsi() -> None:
    rinci = hitung_rinci(INPUT_FIBER, gejala_kasus("K01"), "jaccard")
    assert rinci["jumlah_irisan"] == 4
    assert rinci["jumlah_gabungan"] == 6
    assert rinci["pembilang"] == 4
    assert rinci["penyebut"] == 6
    assert rinci["hasil"] == jaccard_similarity(INPUT_FIBER, gejala_kasus("K01"))


def test_hitung_rinci_weighted_konsisten_dengan_fungsi() -> None:
    rinci = hitung_rinci(INPUT_FIBER, gejala_kasus("K01"), "weighted", BOBOT_GEJALA)
    assert rinci["jumlah_bobot_irisan"] == pytest.approx(6.0)
    assert rinci["jumlah_bobot_gabungan"] == pytest.approx(9.0)
    assert rinci["pembilang"] == pytest.approx(6.0)
    assert rinci["penyebut"] == pytest.approx(9.0)
    assert rinci["hasil"] == weighted_jaccard_similarity(INPUT_FIBER, gejala_kasus("K01"), BOBOT_GEJALA)


def test_hitung_rinci_mode_tidak_dikenal() -> None:
    with pytest.raises(ValueError):
        hitung_rinci(INPUT_FIBER, gejala_kasus("K01"), "cosine")
