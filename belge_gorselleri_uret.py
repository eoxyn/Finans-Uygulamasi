"""Finans uygulamasinin belge icin kesilmis ekran goruntulerini uretir."""

from __future__ import annotations

import ctypes
import json
import subprocess
import sys
from ctypes import wintypes
from pathlib import Path
from time import sleep, time

from PIL import ImageGrab


PROJE_KLASORU = Path(__file__).resolve().parent
GORSEL_KLASORU = PROJE_KLASORU / "gorseller"
TEMEL_BOYUT = (1936, 1048)

SW_MAXIMIZE = 3
WM_CLOSE = 0x0010
VK_RETURN = 0x0D
VK_ESCAPE = 0x1B
VK_CONTROL = 0x11
VK_A = 0x41
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

user32 = ctypes.windll.user32

ACIKLAMALAR = {
    "01_uygulama_genel_bakis.png": "GUI uygulamasinin tam ekran genel gorunumu",
    "02_canli_doviz_kurlari.png": "Canli USD, EUR ve GBP kur bandi",
    "03_finans_ozet_kartlari.png": "Toplam gelir, gider, bakiye ve islem sayisi kartlari",
    "04_yeni_islem_paneli.png": "Yeni gelir veya gider kaydi giris paneli",
    "05_kayitlar_tablosu.png": "Tum gelir ve gider hareketleri tablosu",
    "06_numpy_finansal_analiz.png": "Pandas ve NumPy finansal analiz sonuclari",
    "07_aylik_ozet_tablosu.png": "Aylik gelir, gider ve bakiye ozeti",
    "08_grafik_onizleme_bolumu.png": "Grafik secimi ve bos onizleme alani",
    "09_gelir_turu_secimi.png": "Gelir islem turu secimi",
    "10_gider_turu_secimi.png": "Gider islem turu secimi",
    "11_gelir_ekleme_formu.png": "Gelir kaydi eklenmeden once doldurulmus form",
    "12_gelir_ekleme_sonucu.png": "Gelir kaydi eklendikten sonraki tablo ve ozet",
    "13_gider_ekleme_formu.png": "Gider kaydi eklenmeden once doldurulmus form",
    "14_gider_ekleme_sonucu.png": "Gider kaydi eklendikten sonraki tablo ve ozet",
    "15_gecersiz_tutar_uyarisi.png": "Gecersiz tutar dogrulama uyarisi",
    "16_gecersiz_tarih_uyarisi.png": "Gecersiz tarih dogrulama uyarisi",
    "17_secim_yok_uyarisi.png": "Secim yapmadan silme uyarisi",
    "18_silinecek_kayit_secimi.png": "Silinecek kaydin tablodan secilmesi",
    "19_kayit_silme_sonucu.png": "Secili kayit silindikten sonraki sonuc",
    "20_csv_dosyasi_acma.png": "CSV dosyasi acma iletisim kutusu",
    "21_csv_dosyasi_kaydetme.png": "CSV dosyasi kaydetme iletisim kutusu",
    "22_ornek_veri_yukleme.png": "Ornek veriler yuklendikten sonraki sonuc",
    "23_aylik_cizgi_grafik.png": "Aylik gelir ve gider cizgi grafigi",
    "24_toplam_bar_grafik.png": "Toplam gelir ve gider bar grafigi",
    "25_gelir_gider_pasta_grafik.png": "Gelir ve gider pasta grafigi",
    "26_grafik_kaydetme.png": "Grafigi PNG olarak kaydetme iletisim kutusu",
    "27_konsol_ana_menu.png": "Yedi maddelik konsol ana menusu",
    "28_konsol_gelir_ekleme.png": "Konsol uzerinden gelir ekleme islemi",
    "29_konsol_gider_ekleme.png": "Konsol uzerinden gider ekleme islemi",
    "30_konsol_islemleri_listeleme.png": "Konsol uzerinden islemleri listeleme",
    "31_konsol_finansal_analiz.png": "Konsol finansal analiz sonuclari",
    "32_konsol_grafik_secimi.png": "Konsol grafik secim menusu",
    "33_konsol_csv_kaydetme.png": "Konsol uzerinden CSV kaydetme",
    "34_konsol_cikis.png": "Konsol uygulamasindan cikis",
}


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [("ki", KEYBDINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("union", INPUT_UNION)]


def gorunen_pencereler():
    pencereler = []
    enum_callback = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def pencereyi_ekle(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        uzunluk = user32.GetWindowTextLengthW(hwnd)
        if uzunluk <= 0:
            return True
        baslik = ctypes.create_unicode_buffer(uzunluk + 1)
        user32.GetWindowTextW(hwnd, baslik, uzunluk + 1)
        pencereler.append({"handle": int(hwnd), "baslik": baslik.value})
        return True

    user32.EnumWindows(enum_callback(pencereyi_ekle), 0)
    return pencereler


def pencere_bul(baslik_parcasi, zaman_asimi=10):
    bitis = time() + zaman_asimi
    while time() < bitis:
        for pencere in gorunen_pencereler():
            if baslik_parcasi.lower() in pencere["baslik"].lower():
                return pencere
        sleep(0.2)
    raise RuntimeError(f"Pencere bulunamadi: {baslik_parcasi}")


def uygulama_penceresini_bul():
    for anahtar in ("finansal hesaplama", "finans"):
        try:
            return pencere_bul(anahtar, zaman_asimi=2)
        except RuntimeError:
            continue
    raise RuntimeError("Acik finans uygulamasi penceresi bulunamadi.")


def pencere_konumu(handle):
    dikdortgen = wintypes.RECT()
    user32.GetWindowRect(handle, ctypes.byref(dikdortgen))
    return (
        dikdortgen.left,
        dikdortgen.top,
        dikdortgen.right,
        dikdortgen.bottom,
    )


def pencereyi_one_getir(handle, buyut=False):
    if buyut:
        user32.ShowWindow(handle, SW_MAXIMIZE)
    user32.SetForegroundWindow(handle)
    sleep(0.6)


def pencere_goruntusu(handle):
    return ImageGrab.grab(bbox=pencere_konumu(handle), all_screens=True)


def olcekle(deger, guncel, temel):
    return round(deger * guncel / temel)


def uygulama_koordinati(handle, x, y):
    sol, ust, sag, alt = pencere_konumu(handle)
    genislik = sag - sol
    yukseklik = alt - ust
    return (
        sol + olcekle(x, genislik, TEMEL_BOYUT[0]),
        ust + olcekle(y, yukseklik, TEMEL_BOYUT[1]),
    )


def uygulamaya_tikla(handle, x, y):
    pencereyi_one_getir(handle)
    ekran_x, ekran_y = uygulama_koordinati(handle, x, y)
    user32.SetCursorPos(ekran_x, ekran_y)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    sleep(0.35)


def tusa_bas(vk):
    user32.keybd_event(vk, 0, 0, 0)
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
    sleep(0.1)


def ctrl_a():
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_A, 0, 0, 0)
    user32.keybd_event(VK_A, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
    sleep(0.1)


def metin_yaz(metin):
    girdiler = []
    for karakter in metin:
        kod = ord(karakter)
        girdiler.extend(
            [
                INPUT(
                    type=1,
                    union=INPUT_UNION(
                        ki=KEYBDINPUT(
                            wVk=0,
                            wScan=kod,
                            dwFlags=KEYEVENTF_UNICODE,
                            time=0,
                            dwExtraInfo=None,
                        )
                    ),
                ),
                INPUT(
                    type=1,
                    union=INPUT_UNION(
                        ki=KEYBDINPUT(
                            wVk=0,
                            wScan=kod,
                            dwFlags=KEYEVENTF_UNICODE | KEYEVENTF_KEYUP,
                            time=0,
                            dwExtraInfo=None,
                        )
                    ),
                ),
            ]
        )
    dizi = (INPUT * len(girdiler))(*girdiler)
    user32.SendInput(len(dizi), dizi, ctypes.sizeof(INPUT))
    sleep(0.25)


def alan_doldur(handle, x, y, metin):
    uygulamaya_tikla(handle, x, y)
    ctrl_a()
    metin_yaz(metin)


def uygulama_goruntusu_kaydet(handle, dosya_adi, kirpma=None):
    goruntu = pencere_goruntusu(handle)
    if kirpma:
        genislik, yukseklik = goruntu.size
        kutu = tuple(
            olcekle(deger, genislik if sira % 2 == 0 else yukseklik, TEMEL_BOYUT[sira % 2])
            for sira, deger in enumerate(kirpma)
        )
        goruntu = goruntu.crop(kutu)
    goruntu.save(GORSEL_KLASORU / dosya_adi)


def pencere_goruntusu_kaydet(baslik, dosya_adi):
    pencere = pencere_bul(baslik)
    pencereyi_one_getir(pencere["handle"])
    pencere_goruntusu(pencere["handle"]).save(GORSEL_KLASORU / dosya_adi)
    return pencere["handle"]


def iletisim_kutusunu_yakala(baslik, dosya_adi, kapatma_tusu=VK_ESCAPE):
    pencere_goruntusu_kaydet(baslik, dosya_adi)
    tusa_bas(kapatma_tusu)
    sleep(0.5)


def ilk_bolumleri_yakala(handle):
    uygulama_goruntusu_kaydet(handle, "01_uygulama_genel_bakis.png")
    uygulama_goruntusu_kaydet(handle, "02_canli_doviz_kurlari.png", (755, 34, 1180, 98))
    uygulama_goruntusu_kaydet(handle, "03_finans_ozet_kartlari.png", (25, 91, 1910, 191))
    uygulama_goruntusu_kaydet(handle, "04_yeni_islem_paneli.png", (25, 190, 365, 995))
    uygulama_goruntusu_kaydet(handle, "05_kayitlar_tablosu.png", (365, 190, 1200, 995))
    uygulama_goruntusu_kaydet(handle, "06_numpy_finansal_analiz.png", (1195, 190, 1908, 380))
    uygulama_goruntusu_kaydet(handle, "07_aylik_ozet_tablosu.png", (1195, 375, 1908, 585))
    uygulama_goruntusu_kaydet(handle, "08_grafik_onizleme_bolumu.png", (1195, 575, 1908, 995))


def gui_islemlerini_yakala(handle):
    uygulamaya_tikla(handle, 120, 344)
    uygulama_goruntusu_kaydet(handle, "09_gelir_turu_secimi.png", (35, 285, 350, 375))

    uygulamaya_tikla(handle, 260, 344)
    uygulama_goruntusu_kaydet(handle, "10_gider_turu_secimi.png", (35, 285, 350, 375))

    uygulamaya_tikla(handle, 120, 344)
    alan_doldur(handle, 190, 425, "1500")
    alan_doldur(handle, 190, 503, "2026-04-01")
    alan_doldur(handle, 190, 580, "Belge gelir testi")
    uygulama_goruntusu_kaydet(handle, "11_gelir_ekleme_formu.png", (35, 285, 350, 675))
    uygulamaya_tikla(handle, 195, 640)
    uygulama_goruntusu_kaydet(handle, "12_gelir_ekleme_sonucu.png", (25, 90, 1200, 1040))

    uygulamaya_tikla(handle, 260, 344)
    alan_doldur(handle, 190, 425, "750")
    alan_doldur(handle, 190, 503, "2026-04-02")
    alan_doldur(handle, 190, 580, "Belge gider testi")
    uygulama_goruntusu_kaydet(handle, "13_gider_ekleme_formu.png", (35, 285, 350, 675))
    uygulamaya_tikla(handle, 195, 640)
    uygulama_goruntusu_kaydet(handle, "14_gider_ekleme_sonucu.png", (25, 90, 1200, 1040))

    alan_doldur(handle, 190, 425, "-50")
    alan_doldur(handle, 190, 503, "2026-04-03")
    uygulamaya_tikla(handle, 195, 640)
    iletisim_kutusunu_yakala("Gecersiz Tutar", "15_gecersiz_tutar_uyarisi.png", VK_RETURN)

    alan_doldur(handle, 190, 425, "100")
    alan_doldur(handle, 190, 503, "2026/04/03")
    uygulamaya_tikla(handle, 195, 640)
    iletisim_kutusunu_yakala("Gecersiz Tarih", "16_gecersiz_tarih_uyarisi.png", VK_RETURN)
    alan_doldur(handle, 190, 425, "")
    alan_doldur(handle, 190, 503, "2026-06-04")
    alan_doldur(handle, 190, 580, "")

    uygulamaya_tikla(handle, 195, 688)
    iletisim_kutusunu_yakala("Secim Yok", "17_secim_yok_uyarisi.png", VK_RETURN)

    uygulamaya_tikla(handle, 800, 578)
    uygulama_goruntusu_kaydet(handle, "18_silinecek_kayit_secimi.png", (365, 190, 1200, 620))
    uygulamaya_tikla(handle, 195, 688)
    uygulama_goruntusu_kaydet(handle, "19_kayit_silme_sonucu.png", (25, 90, 1200, 1040))

    uygulamaya_tikla(handle, 195, 780)
    iletisim_kutusunu_yakala("CSV Dosyasi Ac", "20_csv_dosyasi_acma.png")
    uygulamaya_tikla(handle, 195, 825)
    iletisim_kutusunu_yakala("CSV Kaydet", "21_csv_dosyasi_kaydetme.png")

    uygulamaya_tikla(handle, 195, 870)
    uygulama_goruntusu_kaydet(handle, "22_ornek_veri_yukleme.png", (25, 90, 1200, 1040))

    uygulamaya_tikla(handle, 1290, 608)
    uygulamaya_tikla(handle, 1717, 608)
    sleep(3)
    uygulama_goruntusu_kaydet(handle, "23_aylik_cizgi_grafik.png", (1195, 575, 1908, 995))

    uygulamaya_tikla(handle, 1430, 608)
    uygulamaya_tikla(handle, 1717, 608)
    sleep(2)
    uygulama_goruntusu_kaydet(handle, "24_toplam_bar_grafik.png", (1195, 575, 1908, 995))

    uygulamaya_tikla(handle, 1575, 608)
    uygulamaya_tikla(handle, 1717, 608)
    sleep(2)
    uygulama_goruntusu_kaydet(handle, "25_gelir_gider_pasta_grafik.png", (1195, 575, 1908, 995))

    uygulamaya_tikla(handle, 1830, 608)
    iletisim_kutusunu_yakala("Grafik Kaydet", "26_grafik_kaydetme.png")


def konsola_yaz(handle, metin):
    pencereyi_one_getir(handle)
    metin_yaz(metin)
    tusa_bas(VK_RETURN)
    sleep(0.8)


def konsol_islemlerini_yakala():
    komut = (
        f'title Finans Konsol Menusu && cd /d "{PROJE_KLASORU}" '
        f'&& "{sys.executable}" main.py --console'
    )
    surec = subprocess.Popen(
        ["cmd.exe", "/k", komut],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    konsol = pencere_bul("Finans Konsol Menusu", zaman_asimi=15)
    pencereyi_one_getir(konsol["handle"], buyut=True)
    sleep(2)
    pencere_goruntusu(konsol["handle"]).save(GORSEL_KLASORU / "27_konsol_ana_menu.png")

    for deger in ("1", "1111", "2026-04-03", "Belge konsol gelir"):
        konsola_yaz(konsol["handle"], deger)
    pencere_goruntusu(konsol["handle"]).save(GORSEL_KLASORU / "28_konsol_gelir_ekleme.png")

    for deger in ("2", "222", "2026-04-04", "Belge konsol gider"):
        konsola_yaz(konsol["handle"], deger)
    pencere_goruntusu(konsol["handle"]).save(GORSEL_KLASORU / "29_konsol_gider_ekleme.png")

    konsola_yaz(konsol["handle"], "3")
    pencere_goruntusu(konsol["handle"]).save(GORSEL_KLASORU / "30_konsol_islemleri_listeleme.png")

    konsola_yaz(konsol["handle"], "4")
    pencere_goruntusu(konsol["handle"]).save(GORSEL_KLASORU / "31_konsol_finansal_analiz.png")

    konsola_yaz(konsol["handle"], "5")
    pencere_goruntusu(konsol["handle"]).save(GORSEL_KLASORU / "32_konsol_grafik_secimi.png")
    konsola_yaz(konsol["handle"], "9")

    konsola_yaz(konsol["handle"], "6")
    pencere_goruntusu(konsol["handle"]).save(GORSEL_KLASORU / "33_konsol_csv_kaydetme.png")

    konsola_yaz(konsol["handle"], "7")
    sleep(1)
    pencere_goruntusu(konsol["handle"]).save(GORSEL_KLASORU / "34_konsol_cikis.png")
    user32.PostMessageW(konsol["handle"], WM_CLOSE, 0, 0)
    try:
        surec.wait(timeout=5)
    except subprocess.TimeoutExpired:
        surec.terminate()


def verileri_geri_yukle(handle):
    pencereyi_one_getir(handle, buyut=True)
    uygulamaya_tikla(handle, 195, 870)
    sleep(1)


def liste_dosyasi_yaz():
    satirlar = ["BELGE GORSELLERI", "================", ""]
    for dosya_adi, aciklama in ACIKLAMALAR.items():
        satirlar.append(f"{dosya_adi}: {aciklama}")
    (GORSEL_KLASORU / "gorsel_listesi.txt").write_text("\n".join(satirlar), encoding="utf-8")


def main():
    GORSEL_KLASORU.mkdir(exist_ok=True)
    uygulama = uygulama_penceresini_bul()
    pencereyi_one_getir(uygulama["handle"], buyut=True)
    ilk_bolumleri_yakala(uygulama["handle"])
    gui_islemlerini_yakala(uygulama["handle"])
    konsol_islemlerini_yakala()
    verileri_geri_yukle(uygulama["handle"])
    liste_dosyasi_yaz()
    uretilenler = sorted(yol.name for yol in GORSEL_KLASORU.glob("*.png"))
    print(json.dumps({"adet": len(uretilenler), "dosyalar": uretilenler}, ensure_ascii=False))


if __name__ == "__main__":
    main()
