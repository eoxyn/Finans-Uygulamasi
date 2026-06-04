"""Gelir ve gider kayitlarini yoneten fonksiyonlar."""

from __future__ import annotations

from finans_modeli import Islem
from utils import metni_temizle, sayi_kontrol, tarih_kontrol, yeni_id_olustur


def _konsoldan_islem_bilgisi_al(tip):
    """Konsol akisi icin kullanicidan dogrulanmis islem bilgisi alir."""
    while True:
        tutar = input(f"{tip.title()} tutari: ").strip()
        if sayi_kontrol(tutar):
            break
        print("Gecerli ve pozitif bir sayi giriniz.")

    while True:
        tarih = input("Tarih (YYYY-MM-DD): ").strip()
        if tarih_kontrol(tarih):
            break
        print("Tarih formati YYYY-MM-DD olmalidir.")

    aciklama = input("Aciklama: ").strip()
    return float(tutar), tarih, metni_temizle(aciklama)


def _islem_ekle(liste, tip, tutar=None, tarih=None, aciklama=None, diger_liste=None):
    """Ortak gelir/gider ekleme mantigini calistirir."""
    if tutar is None or tarih is None or aciklama is None:
        tutar, tarih, aciklama = _konsoldan_islem_bilgisi_al(tip)

    tum_islemler = liste + (diger_liste or [])
    yeni_islem = Islem(
        yeni_id_olustur(tum_islemler),
        tutar,
        tarih,
        metni_temizle(aciklama),
        tip,
    )
    liste.append(yeni_islem)
    return yeni_islem


def gelir_ekle(gelirler, tutar=None, tarih=None, aciklama=None, giderler=None):
    """Dogrulanmis yeni gelir kaydi olusturur ve listeye ekler."""
    return _islem_ekle(gelirler, "gelir", tutar, tarih, aciklama, giderler)


def gider_ekle(giderler, tutar=None, tarih=None, aciklama=None, gelirler=None):
    """Dogrulanmis yeni gider kaydi olusturur ve listeye ekler."""
    return _islem_ekle(giderler, "gider", tutar, tarih, aciklama, gelirler)


def islemleri_listele(gelirler, giderler):
    """Tum gelir ve gider kayitlarini tarih ve ID sirasiyla listeler."""
    islemler = sorted(gelirler + giderler, key=lambda islem: (islem.tarih, islem.id))
    if not islemler:
        print("Kayitli islem bulunamadi.")
        return []

    print("\n ID | Tarih      | Tip   | Tutar          | Aciklama")
    print("-" * 68)
    for islem in islemler:
        print(islem.ozet_satir())
    return islemler


def islem_sil(gelirler, giderler, id):
    """Verilen ID'ye sahip islemi bulur ve ilgili listeden siler."""
    aranan_id = int(id)
    for liste in (gelirler, giderler):
        for sira, islem in enumerate(liste):
            if islem.id == aranan_id:
                return liste.pop(sira)
    return None
