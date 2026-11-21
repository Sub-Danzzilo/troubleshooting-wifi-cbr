"""Uji siklus 4R (retrieve, reuse, revise, retain) dan persistensi case base."""

import copy

import pytest

from core import cbr_engine, storage
from core.case_base import CASE_BASE_AWAL


def kasus(kasus_id, case_base=None):
    case_base = CASE_BASE_AWAL if case_base is None else case_base
    return next(item for item in case_base if item["id"] == kasus_id)


def test_retrieve_terurut_menurun():
    hasil = cbr_engine.retrieve(["tidak_connect"], CASE_BASE_AWAL)
    skor = [item["skor"] for item in hasil["kandidat"]]
    assert skor == sorted(skor, reverse=True)


def test_retrieve_melewati_kasus_belum_terselesaikan():
    case_base = copy.deepcopy(CASE_BASE_AWAL)
    case_base[0]["status"] = "belum_terselesaikan"
    hasil = cbr_engine.retrieve(case_base[0]["gejala"], case_base)
    assert all(item["kasus"]["id"] != case_base[0]["id"] for item in hasil["kandidat"])


def test_retrieve_menandai_tidak_ada_kecocokan():
    hasil = cbr_engine.retrieve(["lan_nyala"], CASE_BASE_AWAL)
    assert hasil["skor_tertinggi"] == 0.0
    assert hasil["ada_kecocokan"] is False


def test_reuse_menyalin_solusi_apa_adanya():
    kasus_k01 = kasus("K01")
    hasil = cbr_engine.reuse(kasus_k01, ["tidak_connect", "los_merah"])
    assert hasil["solusi"] == kasus_k01["solusi"]
    assert hasil["kategori_solusi"] == kasus_k01["kategori_solusi"]
    assert "tidak_connect" in hasil["penjelasan"]["cocok"]
    assert "internet_mati" in hasil["penjelasan"]["hanya_kasus"]


def test_revise_berhasil_lanjut_retain():
    hasil = cbr_engine.retrieve(kasus("K01")["gejala"], CASE_BASE_AWAL)
    revisi = cbr_engine.revise(hasil, 0, True)
    assert revisi["keputusan"] == "retain"
    assert revisi["kasus_terpilih"]["id"] == hasil["kandidat"][0]["kasus"]["id"]


def test_revise_gagal_ke_kandidat_berikutnya():
    hasil = cbr_engine.retrieve(kasus("K01")["gejala"], CASE_BASE_AWAL)
    revisi = cbr_engine.revise(hasil, 0, False)
    assert revisi["keputusan"] == "kandidat_berikutnya"
    assert revisi["indeks_kandidat"] == 1


def test_revise_kandidat_habis_dan_solusi_baru():
    hasil = cbr_engine.retrieve(kasus("K01")["gejala"], CASE_BASE_AWAL)
    indeks_terakhir = len(hasil["kandidat"]) - 1
    habis = cbr_engine.revise(hasil, indeks_terakhir, False)
    assert habis["keputusan"] == "tidak_ada_kandidat"

    baru = cbr_engine.revise(hasil, indeks_terakhir, False, solusi_baru="Cabut adaptor daya")
    assert baru["keputusan"] == "solusi_baru"
    assert baru["solusi_baru"] == "Cabut adaptor daya"


def test_retain_duplikat_hanya_menaikkan_counter():
    kasus_k01 = kasus("K01")
    jumlah_awal = len(CASE_BASE_AWAL)
    dipakai_awal = kasus_k01["jumlah_dipakai"]

    case_base_baru, info = cbr_engine.retain(
        kasus_k01["gejala"], kasus_k01, kasus_k01["solusi"], "berhasil", CASE_BASE_AWAL
    )

    assert info["aksi"] == "duplikat"
    assert len(case_base_baru) == jumlah_awal
    assert kasus("K01", case_base_baru)["jumlah_dipakai"] == dipakai_awal + 1
    # CASE_BASE_AWAL tidak boleh ikut berubah.
    assert kasus("K01")["jumlah_dipakai"] == dipakai_awal


def test_retain_kasus_baru_menambah_dan_memberi_id():
    gejala_baru = ["lan_nyala", "internet_lambat", "hanya_1_perangkat"]
    case_base_baru, info = cbr_engine.retain(
        gejala_baru, None, ["Cek kabel LAN dan port perangkat"], "berhasil", CASE_BASE_AWAL
    )

    assert info["aksi"] == "ditambahkan"
    assert info["id_kasus"] == "K16"
    assert len(case_base_baru) == len(CASE_BASE_AWAL) + 1
    kasus_baru = case_base_baru[-1]
    assert kasus_baru["sumber"] == "retain"
    assert kasus_baru["kategori_solusi"] == "baru"
    assert kasus_baru["gejala"] == sorted(gejala_baru)


def test_retain_menolak_solusi_kosong():
    with pytest.raises(ValueError):
        cbr_engine.retain(["lan_nyala"], None, [], "berhasil", CASE_BASE_AWAL)


def test_storage_roundtrip(tmp_path, monkeypatch):
    path = tmp_path / "case_base.json"
    monkeypatch.setattr(storage, "PATH_CASE_BASE_JSON", str(path))

    case_base = storage.reset_case_base()
    assert path.exists()

    dimuat = storage.muat_case_base()
    assert len(dimuat) == len(case_base)
    assert dimuat[0]["id"] == "K01"
