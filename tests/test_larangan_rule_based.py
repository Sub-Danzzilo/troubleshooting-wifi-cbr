"""Penjaga batasan dosen: tidak boleh ada mesin inferensi rule-based.

Memindai app.py, core/, dan ui/ lalu gagal bila menemukan pola terlarang.
Folder tests/ sendiri dikecualikan agar nama pola boleh ditulis di sini.
"""

import re
from pathlib import Path

import pytest

from core import cbr_engine

AKAR = Path(__file__).resolve().parent.parent
BERKAS_DIPERIKSA = (
    [AKAR / "app.py"]
    + sorted((AKAR / "core").glob("*.py"))
    + sorted((AKAR / "ui").glob("*.py"))
)

POLA_TERLARANG = [
    (re.compile(r"\bForwardChaining\b"), "class ForwardChaining"),
    (re.compile(r"\bBackwardChaining\b"), "class BackwardChaining"),
    (re.compile(r"\bRuleEngine\b"), "class RuleEngine"),
    (re.compile(r"\bInferenceEngine\b"), "class InferenceEngine"),
    (re.compile(r"\brules\s*="), "struktur bernama rules"),
    (re.compile(r"\bfor\s+\w+\s+in\s+rules\b"), "iterasi atas rules"),
]

# Percabangan yang membandingkan status lampu dengan string kesimpulan.
POLA_LAMPU_KE_KESIMPULAN = re.compile(
    r"if\b[^\n#]*\b(los|pon|power|wlan|lan|status_lampu)\w*[^\n]*[=!]=?[^\n]*[\"']",
    re.IGNORECASE,
)


@pytest.mark.parametrize("berkas", BERKAS_DIPERIKSA, ids=lambda path: path.name)
def test_tidak_ada_pola_rule_based(berkas):
    isi = berkas.read_text(encoding="utf-8")
    for pola, keterangan in POLA_TERLARANG:
        assert not pola.search(isi), f"{berkas.name} memakai pola terlarang: {keterangan}"


@pytest.mark.parametrize("berkas", BERKAS_DIPERIKSA, ids=lambda path: path.name)
def test_tidak_ada_if_lampu_ke_kesimpulan(berkas):
    isi = berkas.read_text(encoding="utf-8")
    assert not POLA_LAMPU_KE_KESIMPULAN.search(isi), (
        f"{berkas.name} membandingkan status lampu dengan string kesimpulan"
    )


@pytest.mark.parametrize("nama", sorted((AKAR / "core").glob("*.py")), ids=lambda path: path.name)
def test_core_tidak_import_streamlit(nama):
    isi = nama.read_text(encoding="utf-8")
    assert "import streamlit" not in isi
    assert "from streamlit" not in isi


@pytest.mark.parametrize(
    "nama,tahap",
    [("retrieve", "retrieve"), ("reuse", "reuse"), ("revise", "revise"), ("retain", "retain")],
)
def test_fungsi_empat_r_ada_dan_berdocstring(nama, tahap):
    fungsi = getattr(cbr_engine, nama, None)
    assert fungsi is not None, f"core.cbr_engine.{nama} tidak ditemukan"
    assert callable(fungsi)
    assert fungsi.__doc__, f"{nama} harus punya docstring"
    assert tahap in fungsi.__doc__.lower(), f"docstring {nama} harus menyebut tahap CBR-nya"
