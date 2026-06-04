"""Ornek proje ciktilarini ureten yardimci script."""

from __future__ import annotations

from pathlib import Path

import matplotlib

from analiz import aylik_analiz, numpy_istatistik, toplam_gelir_gider, verileri_dataframe_yap
from dosya_islemleri import csv_kaydet, csv_oku
from gorsellestirme import aylik_grafik, gelir_gider_bar, pasta_grafik
from utils import para_formatla


PROJE_KLASORU = Path(__file__).resolve().parent
VERI_DOSYASI = PROJE_KLASORU / "veri" / "finans_kayitlari.csv"
CIKTI_KLASORU = PROJE_KLASORU / "cikti"


def ciktilari_uret():
    matplotlib.use("Agg")
    CIKTI_KLASORU.mkdir(parents=True, exist_ok=True)
    gelirler, giderler = csv_oku(VERI_DOSYASI)
    df = verileri_dataframe_yap(gelirler, giderler)
    ozet = toplam_gelir_gider(df)
    istatistik = numpy_istatistik(df)
    aylik = aylik_analiz(df)

    csv_kaydet(CIKTI_KLASORU / "ornek_finans_kayitlari.csv", gelirler, giderler)
    aylik.to_csv(CIKTI_KLASORU / "aylik_analiz.csv", index=False, encoding="utf-8-sig")

    analiz_metni = (
        "Kisisel Finans ve Harcama Takip Sistemi - Ornek Analiz Ciktisi\n"
        "Ogrenci: Mehmet Kaya | 24903057 | YBS\n"
        + "=" * 64
        + "\n"
        f"Toplam Gelir      : {para_formatla(ozet['toplam_gelir'])}\n"
        f"Toplam Gider      : {para_formatla(ozet['toplam_gider'])}\n"
        f"Net Bakiye        : {para_formatla(ozet['bakiye'])}\n"
        f"Islem Sayisi      : {istatistik['islem_sayisi']}\n"
        f"Ortalama Islem    : {para_formatla(istatistik['ortalama'])}\n"
        f"Minimum Tutar     : {para_formatla(istatistik['minimum'])}\n"
        f"Maksimum Tutar    : {para_formatla(istatistik['maksimum'])}\n"
        f"Standart Sapma    : {para_formatla(istatistik['standart_sapma'])}\n"
    )
    (CIKTI_KLASORU / "ornek_analiz_ciktisi.txt").write_text(analiz_metni, encoding="utf-8")

    aylik_grafik(df, CIKTI_KLASORU / "aylik_gelir_gider.png", goster=False)
    gelir_gider_bar(df, CIKTI_KLASORU / "toplam_gelir_gider_bar.png", goster=False)
    pasta_grafik(df, CIKTI_KLASORU / "gelir_gider_pasta.png", goster=False)

    try:
        import matplotlib.pyplot as plt

        plt.close("all")
    except ImportError:
        pass

    print(f"Ciktilar olusturuldu: {CIKTI_KLASORU}")


if __name__ == "__main__":
    ciktilari_uret()
