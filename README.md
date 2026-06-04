# Kisisel Finans ve Harcama Takip Sistemi

**Ogrenci:** Mehmet Kaya  
**Ogrenci No:** 24903057  

## Proje Amaci

Bu proje; kullanicinin gelir ve gider kayitlarini ekleyebildigi, kayitlari CSV dosyasinda saklayabildigi, Pandas ve NumPy ile finansal analiz yapabildigi, Matplotlib/Seaborn ile grafik uretebildigi ve canli doviz kurlarini takip edebildigi moduler bir kisisel finans takip sistemidir. GUI şeklinde tasarlanmasının nedeni şahsi kullanım amacımdır.

Uygulama hem modern Tkinter GUI arayuzu hem de odevde istenen 7 maddelik konsol menusu ile calisir. Projenin tek ana giris noktasi `main.py` dosyasidir.


Projede uygulamayi baslatan tek `main` fonksiyonu `main.py` icindedir.

- GUI calistirma: `python main.py`
- Konsol menusu calistirma: `python main.py --console`
- `arayuz.py` yalnizca Tkinter arayuz sinifini icerir.
- `cikti_uret.py` yalnizca ornek CSV, analiz ve grafik ciktilarini ureten yardimci scripttir.

Bu yapi sayesinde proje icinde iki farkli ana uygulama dosyasi yoktur; tum calisma akisi `main.py` uzerinden yonetilir.

## Dizin Yapisi

```text
Mehmet_Kaya_24903057_YBS/
|-- main.py
|-- arayuz.py
|-- finans_modeli.py
|-- islem_yonetimi.py
|-- dosya_islemleri.py
|-- analiz.py
|-- gorsellestirme.py
|-- utils.py
|-- cikti_uret.py
|-- README.md
|-- veri/
|   `-- finans_kayitlari.csv
|-- cikti/
|   |-- ornek_finans_kayitlari.csv
|   |-- aylik_analiz.csv
|   |-- ornek_analiz_ciktisi.txt
|   |-- aylik_gelir_gider.png
|   |-- toplam_gelir_gider_bar.png
|   `-- gelir_gider_pasta.png
`-- varliklar/
    |-- bayrak_usd.png
    |-- bayrak_eur.png
    `-- bayrak_gbp.png
```

## Modul Gorevleri

| Dosya | Gorev |
| --- | --- |
| `main.py` | Projenin tek ana giris noktasi; GUI veya konsol akisini baslatir. |
| `arayuz.py` | Tkinter tabanli grafiksel kullanici arayuzu ve canli doviz kuru bandi. |
| `finans_modeli.py` | `Islem` sinifi ve nesne tabanli veri modeli. |
| `islem_yonetimi.py` | Gelir/gider ekleme, listeleme ve silme islemleri. |
| `dosya_islemleri.py` | CSV okuma ve CSV kaydetme islemleri. |
| `analiz.py` | Pandas DataFrame donusumu, aylik analiz ve NumPy istatistikleri. |
| `gorsellestirme.py` | Aylik cizgi grafik, toplam bar grafik ve pasta grafik. |
| `utils.py` | ID uretme, tarih kontrolu, sayi kontrolu, para formatlama ve menu yazdirma. |
| `cikti_uret.py` | Teslim icin ornek CSV, analiz ve grafik ciktilarini uretir. |

## Kullanilan Veri Yapilari

Projede iki temel liste kullanilir:

```python
gelirler = []
giderler = []
```

Bu listelerdeki her eleman `finans_modeli.py` dosyasindaki `Islem` sinifindan olusturulan bir nesnedir. Her islem nesnesinde `id`, `tutar`, `tarih`, `aciklama` ve `tip` alanlari bulunur.

## Zorunlu Fonksiyonlar

| Modul | Fonksiyonlar |
| --- | --- |
| `utils.py` | `yeni_id_olustur`, `tarih_kontrol`, `sayi_kontrol`, `menu_goster` |
| `islem_yonetimi.py` | `gelir_ekle`, `gider_ekle`, `islemleri_listele`, `islem_sil` |
| `dosya_islemleri.py` | `csv_kaydet`, `csv_oku` |
| `analiz.py` | `verileri_dataframe_yap`, `toplam_gelir_gider`, `aylik_analiz`, `numpy_istatistik` |
| `gorsellestirme.py` | `aylik_grafik`, `gelir_gider_bar`, `pasta_grafik` |

## Konsol Menu Yapisi

`python main.py --console` komutu ile acilan konsol menusu odevde istenen sira ile korunmustur:

```text
1. Gelir Ekle
2. Gider Ekle
3. Listele
4. Analiz Yap
5. Grafik Goster
6. CSV Kaydet
7. Cikis
```

## GUI Ozellikleri

- Gelir ve gider ekleme
- Kayitlari tablo uzerinde listeleme
- Secili islemi silme
- CSV dosyasi acma ve kaydetme
- Toplam gelir, toplam gider, net bakiye ve islem sayisi kartlari
- Aylik gelir/gider/bakiye tablosu
- NumPy ile ortalama, minimum, maksimum ve standart sapma analizi
- Aylik cizgi, toplam bar ve pasta grafik gosterme/kaydetme
- Internetten alinan canli USD/TRY, EUR/TRY ve GBP/TRY kur bandi

## Canli Doviz Kurlari

GUI uygulamasi acildiginda USD/TRY, EUR/TRY ve GBP/TRY kurlari internet uzerinden otomatik olarak alinir ve arayuzun ust bolumunde gosterilir. Kurlar uygulama acikken her 10 dakikada bir yenilenir. Birinci veri kaynagina ulasilamazsa ikinci bir acik kur servisi otomatik olarak denenir.

Canli kur ozelligi icin API anahtari gerekmez ancak internet baglantisi gereklidir. Kur servislerine ulasilamamasi uygulamanin gelir-gider takip ozelliklerinin calismasini engellemez.

## Kurulum

Python 3.10 veya daha yeni surum onerilir.

```bash
pip install numpy pandas matplotlib seaborn
```

## Calistirma

GUI uygulamasini baslatmak icin:

```bash
python main.py
```

Konsol uygulamasini baslatmak icin:

```bash
python main.py --console
```

Ornek proje ciktilarini yeniden uretmek icin:

```bash
python cikti_uret.py
```
