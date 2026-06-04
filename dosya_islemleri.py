"""CSV okuma ve yazma islemleri."""

from __future__ import annotations

import csv
from pathlib import Path

from finans_modeli import Islem


CSV_ALANLARI = ["id", "tutar", "tarih", "aciklama", "tip"]


def csv_kaydet(dosya_adi, gelirler, giderler):
    """Tum gelir ve gider verilerini belirtilen CSV dosyasina kaydeder."""
    yol = Path(dosya_adi)
    yol.parent.mkdir(parents=True, exist_ok=True)
    islemler = sorted(gelirler + giderler, key=lambda islem: (islem.tarih, islem.id))

    with yol.open("w", newline="", encoding="utf-8-sig") as csv_dosyasi:
        yazici = csv.DictWriter(csv_dosyasi, fieldnames=CSV_ALANLARI)
        yazici.writeheader()
        for islem in islemler:
            yazici.writerow(islem.to_dict())
    return yol


def csv_oku(dosya_adi):
    """CSV dosyasindaki verileri okuyarak gelir ve gider listeleri olusturur."""
    yol = Path(dosya_adi)
    gelirler = []
    giderler = []

    if not yol.exists():
        return gelirler, giderler

    with yol.open("r", newline="", encoding="utf-8-sig") as csv_dosyasi:
        okuyucu = csv.DictReader(csv_dosyasi)
        for satir in okuyucu:
            try:
                islem = Islem.from_dict(satir)
            except (KeyError, ValueError):
                continue

            if islem.tip == "gelir":
                gelirler.append(islem)
            else:
                giderler.append(islem)

    return gelirler, giderler
