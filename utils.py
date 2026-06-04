"""Kisisel finans projesinde kullanilan yardimci fonksiyonlar."""

from __future__ import annotations

from datetime import datetime


def yeni_id_olustur(liste):
    """Verilen islem listesindeki en buyuk ID'nin bir fazlasini dondurur."""
    if not liste:
        return 1
    return max(islem.id for islem in liste) + 1


def tarih_kontrol(tarih):
    """Tarihin YYYY-MM-DD formatinda olup olmadigini kontrol eder."""
    try:
        datetime.strptime(str(tarih).strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def sayi_kontrol(deger):
    """Bir degerin pozitif sayiya donusturulebilir olup olmadigini kontrol eder."""
    try:
        return float(deger) > 0
    except (TypeError, ValueError):
        return False


def para_formatla(tutar):
    """TL tutarlarini okunabilir bicimde bicimlendirir."""
    return f"{float(tutar):,.2f} TL".replace(",", "X").replace(".", ",").replace("X", ".")


def metni_temizle(metin):
    """Bos veya fazla bosluklu aciklamalari standart hale getirir."""
    temiz = " ".join(str(metin).strip().split())
    return temiz if temiz else "Aciklama yok"


def menu_goster():
    """Konsol kullanimi icin ana menuyu ekrana yazdirir."""
    print("\n" + "=" * 48)
    print("Kisisel Finans ve Harcama Takip Sistemi")
    print("=" * 48)
    print("1. Gelir Ekle")
    print("2. Gider Ekle")
    print("3. Listele")
    print("4. Analiz Yap")
    print("5. Grafik Goster")
    print("6. CSV Kaydet")
    print("7. Cikis")
