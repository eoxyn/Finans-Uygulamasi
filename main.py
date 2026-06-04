"""Projenin ana giris noktasi.

Varsayilan olarak GUI acilir. Konsol menusu icin:
python main.py --console
"""

from __future__ import annotations

import sys
from pathlib import Path

from analiz import numpy_istatistik, toplam_gelir_gider, verileri_dataframe_yap
from dosya_islemleri import csv_kaydet, csv_oku
from gorsellestirme import aylik_grafik, gelir_gider_bar, pasta_grafik
from islem_yonetimi import gelir_ekle, gider_ekle, islem_sil, islemleri_listele
from arayuz import FinansGUI
from utils import menu_goster, para_formatla


PROJE_KLASORU = Path(__file__).resolve().parent
VARSAYILAN_CSV = PROJE_KLASORU / "veri" / "finans_kayitlari.csv"


def analiz_yazdir(gelirler, giderler):
    """Konsol ekranina finansal analiz sonuclarini yazdirir."""
    df = verileri_dataframe_yap(gelirler, giderler)
    ozet = toplam_gelir_gider(df)
    istatistik = numpy_istatistik(df)
    print("\nFinansal Ozet")
    print("-" * 36)
    print(f"Toplam Gelir   : {para_formatla(ozet['toplam_gelir'])}")
    print(f"Toplam Gider   : {para_formatla(ozet['toplam_gider'])}")
    print(f"Net Bakiye     : {para_formatla(ozet['bakiye'])}")
    print(f"Ortalama Islem : {para_formatla(istatistik['ortalama'])}")
    print(f"Minimum Tutar  : {para_formatla(istatistik['minimum'])}")
    print(f"Maksimum Tutar : {para_formatla(istatistik['maksimum'])}")
    print(f"Standart Sapma : {para_formatla(istatistik['standart_sapma'])}")


def grafik_goster(gelirler, giderler):
    """Konsol secimine gore Matplotlib grafigi acar."""
    df = verileri_dataframe_yap(gelirler, giderler)
    print("\n1. Aylik Cizgi Grafik")
    print("2. Toplam Bar Grafik")
    print("3. Pasta Grafik")
    secim = input("Grafik secimi: ").strip()
    if secim == "1":
        aylik_grafik(df)
    elif secim == "2":
        gelir_gider_bar(df)
    elif secim == "3":
        pasta_grafik(df)
    else:
        print("Gecersiz grafik secimi.")


def konsol_calistir():
    """Odevde istenen konsol menusunu calistirir."""
    gelirler, giderler = csv_oku(VARSAYILAN_CSV)

    while True:
        menu_goster()
        secim = input("Seciminiz: ").strip()

        try:
            if secim == "1":
                gelir_ekle(gelirler, giderler=giderler)
                print("Gelir kaydi eklendi.")
            elif secim == "2":
                gider_ekle(giderler, gelirler=gelirler)
                print("Gider kaydi eklendi.")
            elif secim == "3":
                islemleri_listele(gelirler, giderler)
            elif secim == "4":
                analiz_yazdir(gelirler, giderler)
            elif secim == "5":
                grafik_goster(gelirler, giderler)
            elif secim == "6":
                csv_kaydet(VARSAYILAN_CSV, gelirler, giderler)
                print(f"CSV kaydedildi: {VARSAYILAN_CSV}")
            elif secim == "7":
                csv_kaydet(VARSAYILAN_CSV, gelirler, giderler)
                print("Veriler kaydedildi. Cikis yapiliyor.")
                break
            elif secim.lower().startswith("sil"):
                silinecek_id = secim.split(maxsplit=1)[1]
                silinen = islem_sil(gelirler, giderler, silinecek_id)
                print("Silindi." if silinen else "ID bulunamadi.")
            else:
                print("Gecersiz secim.")
        except (ValueError, IndexError) as hata:
            print(f"Hata: {hata}")


def gui_calistir():
    """Tkinter arayuzunu baslatir."""
    uygulama = FinansGUI()
    uygulama.mainloop()


def main():
    """Projenin tek ana giris noktasini calistirir."""
    if "--console" in sys.argv:
        konsol_calistir()
    else:
        gui_calistir()


if __name__ == "__main__":
    main()
