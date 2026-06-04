# Kisisel Finans ve Harcama Takip Sistemi

**Ogrenci:** Mehmet Kaya  
**Ogrenci No:** 24903057  

## Proje Amaci

Bu proje; kullanicinin gelir ve gider kayitlarini ekleyebildigi, kayitlari CSV dosyasinda saklayabildigi, Pandas ve NumPy ile finansal analiz yapabildigi, Matplotlib/Seaborn ile grafik uretebildigi ve canli doviz kurlarini takip edebildigi moduler bir kisisel finans takip sistemidir. GUI şeklinde tasarlanmasının nedeni şahsi kullanım amacımdır.

Uygulama hem modern Tkinter GUI arayuzu hem de odevde istenen 7 maddelik konsol menusu ile calisir. Projenin tek ana giris noktasi `main.py` dosyasidir.

### Projenin exe uzantısı için **Releases** kısmına gözatabilirsiniz.

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

## GUI Görselleri
### Genel Arayüz
<img width="1936" height="1048" alt="01_uygulama_genel_bakis" src="https://github.com/user-attachments/assets/f2729b9e-f5b5-4383-99d4-dca1e97d3e07" />

### Canlı Döviz Kurları
USD/TRY, EUR/TRY ve GBP/TRY kurları internet üzerinden otomatik olarak alınır. Kurlar uygulama açıkken belirli aralıklarla yenilenir.

<img width="425" height="64" alt="02_canli_doviz_kurlari" src="https://github.com/user-attachments/assets/01038f96-430e-4805-8fac-7f8f4fde9cb9" />

### Finansal Analiz
<img width="1885" height="100" alt="03_finans_ozet_kartlari" src="https://github.com/user-attachments/assets/d5d9330c-13d6-4158-a9cf-1acbc0135a7c" />

### İşlem Paneli
<img width="340" height="805" alt="04_yeni_islem_paneli" src="https://github.com/user-attachments/assets/6404127c-78a0-4b57-b6fb-6cef7a84d5af" />

### Kayıtlar Tablosu
<img width="835" height="805" alt="05_kayitlar_tablosu" src="https://github.com/user-attachments/assets/88ec9630-4c3a-43af-be65-d40390234426" />

### Finansal Analiz
<img width="713" height="190" alt="06_numpy_finansal_analiz" src="https://github.com/user-attachments/assets/3153c515-144c-4fb3-a6a0-7c8105a591c6" />

### Aylık Özet Tablosu
<img width="713" height="210" alt="07_aylik_ozet_tablosu" src="https://github.com/user-attachments/assets/b9d21ca4-11a5-4859-b234-42d6402d31c2" />

### Grafik Tabloları (Aylık, Bar, Pasta)
<img width="758" height="795" alt="{27CA391D-4D92-4F04-9691-7A7EC4245B64}" src="https://github.com/user-attachments/assets/afcc7028-2f7a-4319-9b51-eb727adcaaa1" />
<img width="745" height="788" alt="{2C312157-8CE4-4DF7-A6C9-7C7CC77003DD}" src="https://github.com/user-attachments/assets/880fe11b-600d-4f3a-859f-4ba05d92ecbd" />
<img width="701" height="772" alt="{304EE8DC-198C-4729-B92E-7EA81EADFD59}" src="https://github.com/user-attachments/assets/43f1c5ed-1aa2-4fd1-b265-97a9f3ecfd72" />

### Gelir/Gider Ekleme
<img width="360" height="723" alt="{2FEBAE9B-B0E2-425C-AD96-A4E8FF4B6263}" src="https://github.com/user-attachments/assets/74b96be1-6e02-4dca-b175-8c82495cc8ee" /> \n
<img width="356" height="779" alt="{C83CE5A2-6006-4F52-AF4D-315E2C3D7D62}" src="https://github.com/user-attachments/assets/514275c2-7715-4d0a-9303-175143a56784" />
<img width="782" height="84" alt="{52225078-254F-4728-9616-C77FBA425586}" src="https://github.com/user-attachments/assets/6e1876cf-2c03-474c-909d-7ebf90bcbb9f" />

### Seçilen Gelir/Giderin Silinmesi
<img width="1178" height="665" alt="{BA524B48-5DDC-41EB-8330-BA0671613CFE}" src="https://github.com/user-attachments/assets/6fa7d97c-a3d3-414f-9a6f-152a8a8d5a34" />

### Kontroller Geçersiz Tutar/Tarih Formatı
<img width="261" height="164" alt="{4668CF41-520F-45D9-BB73-FC73456111F3}" src="https://github.com/user-attachments/assets/ef250f80-62b9-4f56-8c2a-c4ee5133b936" />
<img width="300" height="161" alt="{D78C7468-3CCC-4FF2-8E23-E0115E4C580E}" src="https://github.com/user-attachments/assets/d7fc6802-8fef-4f64-a686-40cd7421e623" />

### Dosya İşlemleri
<img width="319" height="184" alt="{743A2E96-4BDE-496B-A753-E2B70028B658}" src="https://github.com/user-attachments/assets/90d1dc75-9839-4406-9332-af609b835a19" />


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
