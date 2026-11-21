"""Skrip evaluasi retrieval: leave-one-out dan lima skenario baru.

Dijalankan dari root proyek: python -m evaluasi.jalankan_evaluasi

Memakai CASE_BASE_AWAL langsung (bukan data/case_base.json) agar hasil evaluasi
tidak berubah karena kasus hasil retain.
"""

import io
import sys
from collections.abc import Iterable, Sequence
from datetime import date
from pathlib import Path
from typing import Any

from core import cbr_engine
from core.case_base import CASE_BASE_AWAL, Kasus
from core.similarity import hitung_rinci
from evaluasi.skenario_uji import SKENARIO_UJI

PASANGAN_MODE: list[tuple[str, str]] = [
    ("jaccard", "Jaccard"),
    ("weighted", "Weighted Jaccard"),
]
DOKUMEN: Path = Path(__file__).resolve().parent.parent / "docs" / "hasil_evaluasi.md"


def _persen(nilai: float) -> str:
    return f"{nilai * 100:.1f}%"


def _tabel(header: Sequence[str], rows: Iterable[Sequence[object]]) -> str:
    baris = ["| " + " | ".join(header) + " |"]
    baris.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in rows:
        baris.append("| " + " | ".join(str(sel) for sel in row) + " |")
    return "\n".join(baris)


def _akurasi(baris: Sequence[dict[str, Any]], kunci: str) -> float:
    if not baris:
        return 0.0
    return sum(1 for item in baris if item[kunci]) / len(baris)


def _uji_kasus(
    gejala: Iterable[str],
    kategori_harapan: str,
    case_base: list[Kasus],
    mode: str,
) -> dict[str, Any]:
    """Ringkas hasil retrieve satu kasus uji: top-1, skor, dan status benar."""
    hasil = cbr_engine.retrieve(gejala, case_base, mode)
    top = hasil["kandidat"][:3]
    kategori_top1 = top[0]["kasus"]["kategori_solusi"] if top else "-"
    return {
        "top1": top[0]["kasus"]["id"] if top else "-",
        "skor": top[0]["skor"] if top else 0.0,
        "kategori_top1": kategori_top1,
        "benar_top1": kategori_top1 == kategori_harapan,
        "benar_top3": any(
            item["kasus"]["kategori_solusi"] == kategori_harapan for item in top
        ),
    }


def uji_leave_one_out(mode: str) -> list[dict[str, Any]]:
    """Tiap kasus diuji terhadap 14 kasus lain (dirinya dikeluarkan)."""
    baris: list[dict[str, Any]] = []
    for kasus_uji in CASE_BASE_AWAL:
        basis = [kasus for kasus in CASE_BASE_AWAL if kasus["id"] != kasus_uji["id"]]
        ringkas = _uji_kasus(kasus_uji["gejala"], kasus_uji["kategori_solusi"], basis, mode)
        baris.append(
            {
                "kasus_uji": kasus_uji["id"],
                "kategori": kasus_uji["kategori_solusi"],
                **ringkas,
            }
        )
    return baris


def uji_skenario(mode: str) -> list[dict[str, Any]]:
    """Lima skenario baru dicocokkan ke seluruh CASE_BASE_AWAL."""
    baris: list[dict[str, Any]] = []
    for skenario in SKENARIO_UJI:
        ringkas = _uji_kasus(
            skenario["gejala"], skenario["kategori_diharapkan"], CASE_BASE_AWAL, mode
        )
        baris.append(
            {
                "skenario": skenario["id"],
                "deskripsi": skenario["deskripsi"],
                "kategori": skenario["kategori_diharapkan"],
                **ringkas,
            }
        )
    return baris


def _bagian_leave_one_out(baris: Sequence[dict[str, Any]]) -> str:
    rows = [
        (
            item["kasus_uji"],
            item["kategori"],
            item["top1"],
            f"{item['skor']:.4f}",
            item["kategori_top1"],
            "ya" if item["benar_top1"] else "tidak",
            "ya" if item["benar_top3"] else "tidak",
        )
        for item in baris
    ]
    return _tabel(
        ["Kasus uji", "Kategori sebenarnya", "Top-1", "Skor top-1", "Kategori top-1", "Top-1 benar", "Top-3 benar"],
        rows,
    )


def _bagian_skenario(baris: Sequence[dict[str, Any]]) -> str:
    rows = [
        (
            item["skenario"],
            item["deskripsi"],
            item["kategori"],
            item["top1"],
            f"{item['skor']:.4f}",
            item["kategori_top1"],
            "ya" if item["benar_top1"] else "tidak",
            "ya" if item["benar_top3"] else "tidak",
        )
        for item in baris
    ]
    return _tabel(
        ["Skenario", "Deskripsi", "Kategori harapan", "Top-1", "Skor", "Kategori top-1", "Top-1 benar", "Top-3 benar"],
        rows,
    )


def _rinci_skenario() -> list[str]:
    """Rincian hitung Jaccard top-3 untuk tiap skenario (validasi manual)."""
    bagian: list[str] = []
    for skenario in SKENARIO_UJI:
        hasil = cbr_engine.retrieve(skenario["gejala"], CASE_BASE_AWAL, "jaccard")
        bagian.append(f"### {skenario['id']} — {skenario['deskripsi']}")
        bagian.append("")
        for urutan, item in enumerate(hasil["kandidat"][:3], start=1):
            rinci = hitung_rinci(skenario["gejala"], item["kasus"]["gejala"], "jaccard")
            bagian.append(
                f"- **Top-{urutan} {item['kasus']['id']}**: "
                f"A ∩ B = {{{', '.join(rinci['irisan'])}}} ({rinci['jumlah_irisan']} anggota), "
                f"A ∪ B = {{{', '.join(rinci['gabungan'])}}} ({rinci['jumlah_gabungan']} anggota) "
                f"→ {rinci['pembilang']} / {rinci['penyebut']} = **{rinci['hasil']:.4f}**"
            )
        bagian.append("")
    return bagian


def _susun_dokumen(
    ringkasan: Sequence[dict[str, Any]], rinci: Sequence[str]
) -> str:
    baris = [
        "# Hasil Evaluasi",
        "",
        f"Dibuat otomatis oleh `python -m evaluasi.jalankan_evaluasi` pada {date.today().isoformat()}.",
        "Sumber data: `CASE_BASE_AWAL` (15 kasus), bukan `data/case_base.json`, agar kasus hasil",
        "retain tidak memengaruhi hasil.",
        "",
        "## Ringkasan",
        "",
        _tabel(
            ["Pengujian", "Mode", "Akurasi top-1", "Akurasi top-3"],
            [
                ("Leave-one-out", item["label"], _persen(item["loo_top1"]), _persen(item["loo_top3"]))
                for item in ringkasan
            ]
            + [
                ("5 skenario baru", item["label"], _persen(item["skenario_top1"]), _persen(item["skenario_top3"]))
                for item in ringkasan
            ],
        ),
        "",
        "## 1. Leave-one-out (15 kasus)",
        "",
    ]
    for item in ringkasan:
        baris.extend([f"### {item['label']}", "", _bagian_leave_one_out(item["loo"]), ""])

    baris.extend(["## 2. Lima skenario baru", ""])
    for item in ringkasan:
        baris.extend([f"### {item['label']}", "", _bagian_skenario(item["skenario"]), ""])

    baris.extend(["## 3. Kasus yang salah", ""])
    salah = []
    for item in ringkasan:
        for hasil in item["loo"]:
            if not hasil["benar_top1"]:
                salah.append(
                    f"- {item['label']} — kasus uji {hasil['kasus_uji']} ({hasil['kategori']}): "
                    f"top-1 {hasil['top1']} ({hasil['kategori_top1']}, skor {hasil['skor']:.4f})"
                )
        for hasil in item["skenario"]:
            if not hasil["benar_top1"]:
                salah.append(
                    f"- {item['label']} — skenario {hasil['skenario']} ({hasil['kategori']}): "
                    f"top-1 {hasil['top1']} ({hasil['kategori_top1']}, skor {hasil['skor']:.4f})"
                )
    baris.extend(salah or ["Tidak ada kasus top-1 yang salah pada pengujian ini."])
    baris.extend(["", "## 4. Perhitungan rinci skenario (Jaccard)", ""])
    baris.extend(rinci)
    baris.extend(
        [
            "## 5. Catatan",
            "",
            "- Leave-one-out menguji apakah kasus yang dikeluarkan kembali dikenali kategorinya",
            "  dari 14 kasus lain. Cara ini mengukur konsistensi case base, bukan performa pada",
            "  keluhan nyata.",
            "- Lima skenario dibuat dari pola gejala yang mirip dengan kasus awal, sehingga akurasi",
            "  yang tinggi belum tentu berlaku untuk keluhan yang sangat berbeda.",
            "- Weighted Jaccard dapat mengubah urutan kandidat karena gejala lampu abnormal berbobot",
            "  2.0 dan gejala kondisi normal berbobot 0.5.",
            "- Perhitungan rinci di bagian 4 memakai fungsi `core.similarity.hitung_rinci` yang sama",
            "  dengan yang ditampilkan aplikasi, sehingga bisa dicocokkan dengan hitungan tangan",
            "  di `docs/validasi_manual.md`.",
            "",
        ]
    )
    return "\n".join(baris)


def main() -> None:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ringkasan: list[dict[str, Any]] = []
    for mode, label in PASANGAN_MODE:
        loo = uji_leave_one_out(mode)
        skenario = uji_skenario(mode)
        ringkasan.append(
            {
                "label": label,
                "loo": loo,
                "skenario": skenario,
                "loo_top1": _akurasi(loo, "benar_top1"),
                "loo_top3": _akurasi(loo, "benar_top3"),
                "skenario_top1": _akurasi(skenario, "benar_top1"),
                "skenario_top3": _akurasi(skenario, "benar_top3"),
            }
        )

    print("Ringkasan evaluasi retrieval")
    print(_tabel(
        ["Pengujian", "Mode", "Top-1", "Top-3"],
        [(item["label"], "leave-one-out", _persen(item["loo_top1"]), _persen(item["loo_top3"])) for item in ringkasan]
        + [(item["label"], "5 skenario", _persen(item["skenario_top1"]), _persen(item["skenario_top3"])) for item in ringkasan],
    ))
    print()

    rinci = _rinci_skenario()
    print("Perhitungan rinci skenario (Jaccard)")
    print("\n".join(rinci))

    DOKUMEN.write_text(_susun_dokumen(ringkasan, rinci), encoding="utf-8")
    print(f"Hasil lengkap ditulis ke {DOKUMEN}")


if __name__ == "__main__":
    main()
