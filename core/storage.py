"""Persistensi case base ke data/case_base.json.

Case base asli (CASE_BASE_AWAL) tidak pernah diubah; semua fungsi bekerja pada
salinan (copy) sehingga kasus awal tetap utuh selama runtime.
"""

import copy
import json
import os

from core.case_base import CASE_BASE_AWAL, PATH_CASE_BASE_JSON


def simpan_case_base(case_base):
    """Tulis case base ke JSON (UTF-8, indent 2) agar teks Indonesia terbaca."""
    folder = os.path.dirname(PATH_CASE_BASE_JSON)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(PATH_CASE_BASE_JSON, "w", encoding="utf-8") as berkas:
        json.dump(case_base, berkas, indent=2, ensure_ascii=False)
        berkas.write("\n")


def reset_case_base():
    """Timpa JSON dengan salinan CASE_BASE_AWAL, lalu kembalikan salinan itu."""
    case_base = copy.deepcopy(CASE_BASE_AWAL)
    simpan_case_base(case_base)
    return case_base


def muat_case_base():
    """Muat case base dari JSON.

    Bila berkas tidak ada atau rusak, case base dibuat ulang dari
    CASE_BASE_AWAL dan langsung disimpan ke disk.
    """
    try:
        with open(PATH_CASE_BASE_JSON, "r", encoding="utf-8") as berkas:
            case_base = json.load(berkas)
        if isinstance(case_base, list) and case_base:
            return case_base
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        pass
    return reset_case_base()
