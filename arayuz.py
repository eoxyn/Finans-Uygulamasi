"""Kisisel Finans ve Harcama Takip Sistemi GUI uygulamasi."""

from __future__ import annotations

import json
import threading
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.error import URLError
from urllib.request import Request, urlopen

from analiz import aylik_analiz, numpy_istatistik, toplam_gelir_gider, verileri_dataframe_yap
from dosya_islemleri import csv_kaydet, csv_oku
from islem_yonetimi import gelir_ekle, gider_ekle, islem_sil
from utils import para_formatla, sayi_kontrol, tarih_kontrol


PROJE_KLASORU = Path(__file__).resolve().parent
VARSAYILAN_CSV = PROJE_KLASORU / "veri" / "finans_kayitlari.csv"
BAYRAK_KLASORU = PROJE_KLASORU / "varliklar"
KUR_PARITELERI = (
    ("USD", "USD-TRY"),
    ("EUR", "EUR-TRY"),
    ("GBP", "GBP-TRY"),
)

RENK = {
    "arka": "#f4f7fb",
    "panel": "#ffffff",
    "panel_ikincil": "#f8fafc",
    "kart": "#ffffff",
    "metin": "#0f172a",
    "ikincil_metin": "#64748b",
    "cizgi": "#dbe3ef",
    "mavi": "#2563eb",
    "mavi_koyu": "#1d4ed8",
    "gelir": "#15803d",
    "gelir_acik": "#dcfce7",
    "gider": "#b91c1c",
    "gider_acik": "#fee2e2",
    "bilgi": "#0369a1",
    "uyari": "#b45309",
    "beyaz": "#ffffff",
}


class FinansGUI(tk.Tk):
    """Tkinter ile gelistirilmis finans takip arayuzu."""

    def __init__(self):
        super().__init__()
        self.title("Kişisel Finansal Hesaplama")
        self.geometry("1480x800")
        self.minsize(1240, 700)
        self.configure(bg=RENK["arka"])

        self.gelirler, self.giderler = csv_oku(VARSAYILAN_CSV)
        self.grafik_canvas = None
        self.tip_butonlari = {}
        self.grafik_butonlari = {}
        self.kur_etiketleri = {}
        self.bayrak_gorselleri = {}

        self.tip_var = tk.StringVar(value="gelir")
        self.tutar_var = tk.StringVar()
        self.tarih_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.aciklama_var = tk.StringVar()
        self.grafik_turu_var = tk.StringVar(value="Aylik Cizgi")
        self.durum_var = tk.StringVar(value="Hazir")
        self.kur_durum_var = tk.StringVar(value="")

        self._stil_kur()
        self._arayuzu_kur()
        self._yenile()
        self._kur_bilgisi_yukle()

    def _stil_kur(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        self.option_add("*Font", ("Segoe UI", 10))
        self.option_add("*TCombobox*Listbox.background", RENK["panel"])
        self.option_add("*TCombobox*Listbox.foreground", RENK["metin"])
        self.option_add("*TCombobox*Listbox.selectBackground", RENK["mavi"])
        self.option_add("*TCombobox*Listbox.selectForeground", RENK["beyaz"])

        style.configure("TFrame", background=RENK["arka"])
        style.configure("Panel.TFrame", background=RENK["panel"], relief="flat")
        style.configure("Card.TFrame", background=RENK["kart"], relief="flat")
        style.configure("TLabel", background=RENK["arka"], foreground=RENK["metin"], font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background=RENK["panel"], foreground=RENK["metin"], font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=RENK["panel"], foreground=RENK["ikincil_metin"], font=("Segoe UI", 9))
        style.configure("Title.TLabel", background=RENK["arka"], foreground=RENK["metin"], font=("Segoe UI Semibold", 22))
        style.configure("CardTitle.TLabel", background=RENK["kart"], foreground=RENK["ikincil_metin"], font=("Segoe UI Semibold", 12))
        style.configure("CardValue.TLabel", background=RENK["kart"], foreground=RENK["metin"], font=("Segoe UI Semibold", 30))
        style.configure("TButton", font=("Segoe UI Semibold", 10), padding=(13, 9), borderwidth=0)
        style.map("TButton", background=[("active", RENK["mavi_koyu"])], foreground=[("active", RENK["beyaz"])])
        style.configure("Primary.TButton", background=RENK["mavi"], foreground=RENK["beyaz"])
        style.configure("Success.TButton", background=RENK["gelir"], foreground=RENK["beyaz"])
        style.configure("Danger.TButton", background=RENK["gider"], foreground=RENK["beyaz"])
        style.configure("Ghost.TButton", background=RENK["panel_ikincil"], foreground=RENK["metin"])
        style.configure(
            "TEntry",
            fieldbackground=RENK["panel_ikincil"],
            foreground=RENK["metin"],
            insertcolor=RENK["metin"],
            bordercolor=RENK["cizgi"],
            lightcolor=RENK["cizgi"],
            darkcolor=RENK["cizgi"],
            padding=9,
        )
        style.configure(
            "Treeview",
            background=RENK["panel"],
            foreground=RENK["metin"],
            fieldbackground=RENK["panel"],
            rowheight=34,
            bordercolor=RENK["cizgi"],
            lightcolor=RENK["cizgi"],
            darkcolor=RENK["cizgi"],
        )
        style.configure("Treeview.Heading", background="#e8eef7", foreground=RENK["metin"], font=("Segoe UI Semibold", 10))
        style.map("Treeview", background=[("selected", RENK["mavi"])], foreground=[("selected", RENK["beyaz"])])

    def _arayuzu_kur(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ust = ttk.Frame(self, padding=(28, 12, 28, 4))
        ust.grid(row=0, column=0, sticky="ew")
        ust.columnconfigure(0, weight=1)
        self._kur_bandi_ekle(ust)

        kartlar = ttk.Frame(self, padding=(28, 8, 28, 8))
        kartlar.grid(row=1, column=0, sticky="ew")
        for kolon in range(4):
            kartlar.columnconfigure(kolon, weight=1)
        self.kart_etiketleri = {}
        self._kart_ekle(kartlar, 0, "Toplam Gelir", "gelir", RENK["gelir"])
        self._kart_ekle(kartlar, 1, "Toplam Gider", "gider", RENK["gider"])
        self._kart_ekle(kartlar, 2, "Net Bakiye", "bakiye", RENK["bilgi"])
        self._kart_ekle(kartlar, 3, "Islem Sayisi", "sayi", RENK["uyari"])

        govde = ttk.Frame(self, padding=(28, 8, 28, 20))
        govde.grid(row=2, column=0, sticky="nsew")
        govde.columnconfigure(0, weight=0)
        govde.columnconfigure(1, weight=3)
        govde.columnconfigure(2, weight=2)
        govde.rowconfigure(0, weight=1)

        self._form_paneli(govde)
        self._tablo_paneli(govde)
        self._analiz_grafik_paneli(govde)

        alt = ttk.Frame(self, padding=(28, 0, 28, 12))
        alt.grid(row=3, column=0, sticky="ew")
        ttk.Label(alt, textvariable=self.durum_var, background=RENK["arka"], foreground=RENK["ikincil_metin"]).pack(anchor="w")

    def _kart_ekle(self, ana, kolon, baslik, anahtar, renk):
        kart = ttk.Frame(ana, style="Card.TFrame", padding=16)
        kart.grid(row=0, column=kolon, sticky="ew", padx=(0 if kolon == 0 else 10, 0))
        ttk.Label(kart, text=baslik, style="CardTitle.TLabel").pack(anchor="w")
        deger = ttk.Label(kart, text="0", style="CardValue.TLabel", foreground=renk)
        deger.pack(anchor="w", pady=(7, 0))
        self.kart_etiketleri[anahtar] = deger

    def _kur_bandi_ekle(self, ana):
        gri = "#e8eef7"
        bant = tk.Frame(
            ana,
            bg=gri,
            highlightbackground=RENK["cizgi"],
            highlightthickness=1,
        )
        bant.grid(row=0, column=0)

        for ulke, parite in KUR_PARITELERI:
            hucre = tk.Frame(bant, bg=gri)
            hucre.pack(side="left", padx=(10, 10), pady=8)
            self._bayrak_etiketi(hucre, ulke, gri).pack(side="left", padx=(0, 6))
            deger = tk.Label(
                hucre,
                text="...",
                bg=gri,
                fg=RENK["mavi_koyu"],
                font=("Segoe UI Semibold", 12),
            )
            deger.pack(side="left")
            self.kur_etiketleri[parite] = deger

    def _bayrak_etiketi(self, ana, ulke, arkaplan):
        yol = BAYRAK_KLASORU / f"bayrak_{ulke.lower()}.png"
        try:
            gorsel = tk.PhotoImage(file=str(yol))
            self.bayrak_gorselleri[ulke] = gorsel
            return tk.Label(ana, image=gorsel, bg=arkaplan, borderwidth=0)
        except tk.TclError:
            return tk.Label(
                ana,
                text=ulke,
                bg=arkaplan,
                fg=RENK["metin"],
                font=("Segoe UI Semibold", 9),
            )

    @staticmethod
    def _kur_formatla(deger):
        return f"{deger:,.2f} TL".replace(",", "X").replace(".", ",").replace("X", ".")

    @staticmethod
    def _kur_al(taban):
        """taban para biriminin (USD/EUR/GBP) TL karsiligini doner."""
        kaynaklar = (
            ("rates", f"https://open.er-api.com/v6/latest/{taban}"),
            (
                "nested",
                f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest"
                f"/v1/currencies/{taban.lower()}.json",
            ),
        )
        for tip, url in kaynaklar:
            try:
                istek = Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urlopen(istek, timeout=8) as cevap:
                    veri = json.loads(cevap.read().decode("utf-8", errors="ignore"))
            except (URLError, TimeoutError, OSError, ValueError):
                continue
            if tip == "rates":
                deger = (veri.get("rates") or {}).get("TRY")
            else:
                deger = (veri.get(taban.lower()) or {}).get("try")
            if deger:
                return float(deger)

        raise ValueError("Kur degeri alinamadi.")

    def _kur_bilgisi_yukle(self):
        thread = threading.Thread(target=self._kur_bilgisi_yukle_thread, daemon=True)
        thread.start()

    def _kur_bilgisi_yukle_thread(self):
        kurlar = {}
        hata_var = False
        for ulke, parite in KUR_PARITELERI:
            try:
                kurlar[parite] = self._kur_al(ulke)
            except (URLError, TimeoutError, OSError, ValueError):
                hata_var = True
        self.after(0, self._kur_bilgisi_guncelle, kurlar, hata_var)

    def _kur_bilgisi_guncelle(self, kurlar, hata_var):
        for parite, deger in kurlar.items():
            if parite in self.kur_etiketleri:
                self.kur_etiketleri[parite].configure(text=self._kur_formatla(deger))

        if kurlar:
            self.kur_durum_var.set("")
        elif hata_var:
            self.kur_durum_var.set("")

        self.after(600000, self._kur_bilgisi_yukle)

    def _segment_buton_ekle(self, ana, metin, deger, komut, sozluk):
        buton = tk.Button(
            ana,
            text=metin,
            command=lambda: komut(deger),
            bd=1,
            relief="solid",
            cursor="hand2",
            font=("Segoe UI Semibold", 10),
            padx=13,
            pady=9,
            highlightthickness=1,
            highlightbackground=RENK["cizgi"],
        )
        buton.pack(side="left", fill="x", expand=True, padx=(0, 6))
        sozluk[deger] = buton
        return buton

    def _segment_renk_yenile(self, sozluk, aktif_deger, aktif_renk=RENK["mavi"]):
        for deger, buton in sozluk.items():
            secili = deger == aktif_deger
            buton.configure(
                bg=aktif_renk if secili else "#e8eef7",
                fg=RENK["beyaz"] if secili else RENK["metin"],
                activebackground=RENK["mavi_koyu"] if secili else "#dbe3ef",
                activeforeground=RENK["beyaz"] if secili else RENK["metin"],
                highlightbackground=aktif_renk if secili else RENK["cizgi"],
            )

    def _tip_sec(self, tip):
        self.tip_var.set(tip)
        aktif_renk = RENK["gelir"] if tip == "gelir" else RENK["gider"]
        self._segment_renk_yenile(self.tip_butonlari, tip, aktif_renk)

    def _grafik_sec(self, grafik_turu):
        self.grafik_turu_var.set(grafik_turu)
        self._segment_renk_yenile(self.grafik_butonlari, grafik_turu, RENK["mavi"])

    def _form_paneli(self, ana):
        panel = ttk.Frame(ana, style="Panel.TFrame", padding=18)
        panel.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="Yeni Islem", style="Panel.TLabel", font=("Segoe UI Semibold", 15)).grid(row=0, column=0, sticky="w")
        ttk.Label(panel, text="Kaydi gir, tablo ve analizler aninda guncellensin.", style="Muted.TLabel").grid(
            row=1,
            column=0,
            sticky="w",
            pady=(4, 10),
        )

        alanlar = [
            ("Tip", "tip"),
            ("Tutar", "tutar"),
            ("Tarih", "tarih"),
            ("Aciklama", "aciklama"),
        ]
        for sira, (etiket, _) in enumerate(alanlar, start=2):
            ttk.Label(panel, text=etiket, style="Muted.TLabel").grid(row=sira * 2 - 1, column=0, sticky="w", pady=(14, 4))

        tip_segment = tk.Frame(panel, bg=RENK["panel"])
        tip_segment.grid(row=4, column=0, sticky="ew")
        self._segment_buton_ekle(tip_segment, "Gelir", "gelir", self._tip_sec, self.tip_butonlari)
        self._segment_buton_ekle(tip_segment, "Gider", "gider", self._tip_sec, self.tip_butonlari)
        self._tip_sec(self.tip_var.get())

        ttk.Entry(panel, textvariable=self.tutar_var, width=28).grid(row=6, column=0, sticky="ew")
        ttk.Entry(panel, textvariable=self.tarih_var, width=28).grid(row=8, column=0, sticky="ew")
        ttk.Entry(panel, textvariable=self.aciklama_var, width=28).grid(row=10, column=0, sticky="ew")

        ttk.Button(panel, text="Islemi Kaydet", command=self._islem_kaydet, style="Success.TButton").grid(row=11, column=0, sticky="ew", pady=(20, 8))
        ttk.Button(panel, text="Secili Islemi Sil", command=self._secili_sil, style="Danger.TButton").grid(row=12, column=0, sticky="ew", pady=4)
        ttk.Label(panel, text="Dosya Islemleri", style="Muted.TLabel").grid(row=13, column=0, sticky="w", pady=(22, 4))
        ttk.Button(panel, text="CSV Ac", command=self._csv_ac, style="Ghost.TButton").grid(row=14, column=0, sticky="ew", pady=4)
        ttk.Button(panel, text="CSV Kaydet", command=self._csv_kaydet, style="Primary.TButton").grid(row=15, column=0, sticky="ew", pady=4)
        ttk.Button(panel, text="Ornek Veri Yukle", command=self._ornek_veri_yukle, style="Ghost.TButton").grid(row=16, column=0, sticky="ew", pady=4)

    def _tablo_paneli(self, ana):
        panel = ttk.Frame(ana, style="Panel.TFrame", padding=18)
        panel.grid(row=0, column=1, sticky="nsew", padx=(0, 14))
        panel.rowconfigure(1, weight=1)
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="Kayitlar", style="Panel.TLabel", font=("Segoe UI Semibold", 15)).grid(row=0, column=0, sticky="w")
        ttk.Label(panel, text="Tum gelir ve gider hareketleri", style="Muted.TLabel").grid(row=0, column=0, sticky="e")
        kolonlar = ("id", "tarih", "tip", "tutar", "aciklama")
        self.tablo = ttk.Treeview(panel, columns=kolonlar, show="headings", selectmode="browse")
        self.tablo.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        self.tablo.heading("id", text="ID")
        self.tablo.heading("tarih", text="Tarih")
        self.tablo.heading("tip", text="Tip")
        self.tablo.heading("tutar", text="Tutar")
        self.tablo.heading("aciklama", text="Aciklama")
        self.tablo.column("id", width=54, anchor="center")
        self.tablo.column("tarih", width=112, anchor="center")
        self.tablo.column("tip", width=76, anchor="center")
        self.tablo.column("tutar", width=130, anchor="e")
        self.tablo.column("aciklama", width=280, anchor="w")
        self.tablo.tag_configure("gelir", background=RENK["gelir_acik"], foreground="#14532d")
        self.tablo.tag_configure("gider", background=RENK["gider_acik"], foreground="#7f1d1d")

        kaydir = ttk.Scrollbar(panel, orient="vertical", command=self.tablo.yview)
        kaydir.grid(row=1, column=1, sticky="ns", pady=(12, 0))
        self.tablo.configure(yscrollcommand=kaydir.set)

    def _analiz_grafik_paneli(self, ana):
        panel = ttk.Frame(ana, style="Panel.TFrame", padding=18)
        panel.grid(row=0, column=2, sticky="nsew")
        panel.rowconfigure(5, weight=1, minsize=245)
        panel.columnconfigure(0, weight=1)

        ttk.Label(panel, text="Analiz ve Grafik", style="Panel.TLabel", font=("Segoe UI Semibold", 15)).grid(row=0, column=0, sticky="w")
        ttk.Label(panel, text="Pandas, NumPy ve Matplotlib ciktilari", style="Muted.TLabel").grid(row=0, column=0, sticky="e")
        self.analiz_metni = tk.Text(
            panel,
            height=6,
            bg=RENK["panel_ikincil"],
            fg=RENK["metin"],
            insertbackground=RENK["metin"],
            relief="flat",
            font=("Consolas", 10),
            padx=12,
            pady=10,
        )
        self.analiz_metni.grid(row=1, column=0, sticky="ew", pady=(12, 10))
        self.analiz_metni.configure(state="disabled")

        ttk.Label(panel, text="Aylik Ozet", style="Muted.TLabel").grid(row=2, column=0, sticky="w")
        self.aylik_tablo = ttk.Treeview(panel, columns=("ay", "gelir", "gider", "bakiye"), show="headings", height=4)
        self.aylik_tablo.grid(row=3, column=0, sticky="ew", pady=(6, 10))
        for kolon, baslik in (("ay", "Ay"), ("gelir", "Gelir"), ("gider", "Gider"), ("bakiye", "Bakiye")):
            self.aylik_tablo.heading(kolon, text=baslik)
            self.aylik_tablo.column(kolon, anchor="center", width=90)

        grafik_kontrol = ttk.Frame(panel, style="Panel.TFrame")
        grafik_kontrol.grid(row=4, column=0, sticky="ew")
        grafik_segment = tk.Frame(grafik_kontrol, bg=RENK["panel"])
        grafik_segment.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self._segment_buton_ekle(grafik_segment, "Aylik", "Aylik Cizgi", self._grafik_sec, self.grafik_butonlari)
        self._segment_buton_ekle(grafik_segment, "Bar", "Toplam Bar", self._grafik_sec, self.grafik_butonlari)
        self._segment_buton_ekle(grafik_segment, "Pasta", "Pasta", self._grafik_sec, self.grafik_butonlari)
        self._grafik_sec(self.grafik_turu_var.get())
        ttk.Button(grafik_kontrol, text="Goster", command=self._grafik_ciz, style="Primary.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(grafik_kontrol, text="Kaydet", command=self._grafik_kaydet, style="Ghost.TButton").pack(side="left")

        self.grafik_alani = ttk.Frame(panel, style="Panel.TFrame")
        self.grafik_alani.grid(row=5, column=0, sticky="nsew", pady=(8, 0))
        self._grafik_bos_mesaj()

    def _grafik_bos_mesaj(self):
        for widget in self.grafik_alani.winfo_children():
            widget.destroy()
        kutu = tk.Frame(
            self.grafik_alani,
            bg=RENK["panel_ikincil"],
            highlightbackground=RENK["cizgi"],
            highlightthickness=1,
        )
        kutu.pack(fill="both", expand=True)
        tk.Label(
            kutu,
            text="Grafik onizlemesi",
            bg=RENK["panel_ikincil"],
            fg=RENK["metin"],
            font=("Segoe UI Semibold", 13),
        ).pack(pady=(42, 4))
        tk.Label(
            kutu,
            text="'Goster' dugmesine basinca secilen grafik burada acilir.",
            bg=RENK["panel_ikincil"],
            fg=RENK["ikincil_metin"],
            font=("Segoe UI", 10),
        ).pack()

    def _islem_kaydet(self):
        tutar = self.tutar_var.get().strip()
        tarih = self.tarih_var.get().strip()
        aciklama = self.aciklama_var.get().strip()
        tip = self.tip_var.get()

        if not sayi_kontrol(tutar):
            messagebox.showerror("Gecersiz Tutar", "Tutar pozitif bir sayi olmalidir.")
            return
        if not tarih_kontrol(tarih):
            messagebox.showerror("Gecersiz Tarih", "Tarih formati YYYY-MM-DD olmalidir.")
            return

        try:
            if tip == "gelir":
                yeni_islem = gelir_ekle(self.gelirler, tutar, tarih, aciklama, self.giderler)
            else:
                yeni_islem = gider_ekle(self.giderler, tutar, tarih, aciklama, self.gelirler)
        except ValueError as hata:
            messagebox.showerror("Kayit Hatasi", str(hata))
            return

        self.tutar_var.set("")
        self.aciklama_var.set("")
        self.durum_var.set(f"Islem eklendi: ID {yeni_islem.id}")
        self._yenile()

    def _secili_sil(self):
        secim = self.tablo.selection()
        if not secim:
            messagebox.showwarning("Secim Yok", "Silmek icin tablodan bir islem seciniz.")
            return
        islem_id = int(self.tablo.item(secim[0], "values")[0])
        silinen = islem_sil(self.gelirler, self.giderler, islem_id)
        if silinen is None:
            messagebox.showerror("Bulunamadi", "Secilen islem bulunamadi.")
            return
        self.durum_var.set(f"Silindi: ID {silinen.id}")
        self._yenile()

    def _csv_ac(self):
        dosya = filedialog.askopenfilename(
            title="CSV Dosyasi Ac",
            filetypes=[("CSV Dosyalari", "*.csv"), ("Tum Dosyalar", "*.*")],
            initialdir=PROJE_KLASORU / "veri",
        )
        if not dosya:
            return
        self.gelirler, self.giderler = csv_oku(dosya)
        self.durum_var.set(f"CSV okundu: {Path(dosya).name}")
        self._yenile()

    def _csv_kaydet(self):
        dosya = filedialog.asksaveasfilename(
            title="CSV Kaydet",
            defaultextension=".csv",
            filetypes=[("CSV Dosyalari", "*.csv")],
            initialfile="finans_kayitlari.csv",
            initialdir=PROJE_KLASORU / "veri",
        )
        if not dosya:
            return
        csv_kaydet(dosya, self.gelirler, self.giderler)
        self.durum_var.set(f"CSV kaydedildi: {Path(dosya).name}")

    def _ornek_veri_yukle(self):
        self.gelirler.clear()
        self.giderler.clear()
        ornekler = [
            ("gelir", 28500, "2026-01-05", "Maas"),
            ("gider", 9500, "2026-01-08", "Kira"),
            ("gider", 3200, "2026-01-18", "Market"),
            ("gelir", 4200, "2026-02-10", "Freelance proje"),
            ("gider", 2100, "2026-02-14", "Faturalar"),
            ("gelir", 29000, "2026-03-05", "Maas"),
            ("gider", 4500, "2026-03-20", "Ulasim ve sosyal"),
        ]
        for tip, tutar, tarih, aciklama in ornekler:
            if tip == "gelir":
                gelir_ekle(self.gelirler, tutar, tarih, aciklama, self.giderler)
            else:
                gider_ekle(self.giderler, tutar, tarih, aciklama, self.gelirler)
        csv_kaydet(VARSAYILAN_CSV, self.gelirler, self.giderler)
        self.durum_var.set("Ornek veri yuklendi ve varsayilan CSV guncellendi.")
        self._yenile()

    def _veri_df(self):
        return verileri_dataframe_yap(self.gelirler, self.giderler)

    def _yenile(self):
        df = self._veri_df()
        ozet = toplam_gelir_gider(df)
        stats = numpy_istatistik(df)
        self.kart_etiketleri["gelir"].configure(text=para_formatla(ozet["toplam_gelir"]))
        self.kart_etiketleri["gider"].configure(text=para_formatla(ozet["toplam_gider"]))
        bakiye_rengi = RENK["gelir"] if ozet["bakiye"] >= 0 else RENK["gider"]
        self.kart_etiketleri["bakiye"].configure(text=para_formatla(ozet["bakiye"]), foreground=bakiye_rengi)
        self.kart_etiketleri["sayi"].configure(text=str(stats["islem_sayisi"]))
        self._tablo_yenile()
        self._analiz_yenile(df, ozet, stats)
        self._aylik_yenile(df)

    def _tablo_yenile(self):
        for satir in self.tablo.get_children():
            self.tablo.delete(satir)
        islemler = sorted(self.gelirler + self.giderler, key=lambda islem: (islem.tarih, islem.id))
        for islem in islemler:
            tutar_metni = para_formatla(islem.tutar)
            self.tablo.insert(
                "",
                "end",
                values=(islem.id, islem.tarih, islem.tip, tutar_metni, islem.aciklama),
                tags=(islem.tip,),
            )

    def _analiz_yenile(self, df, ozet, stats):
        metin = (
            f"Toplam Gelir      : {para_formatla(ozet['toplam_gelir'])}\n"
            f"Toplam Gider      : {para_formatla(ozet['toplam_gider'])}\n"
            f"Net Bakiye        : {para_formatla(ozet['bakiye'])}\n"
            f"Ortalama Islem    : {para_formatla(stats['ortalama'])}\n"
            f"En Kucuk / Buyuk  : {para_formatla(stats['minimum'])} / {para_formatla(stats['maksimum'])}\n"
            f"Standart Sapma    : {para_formatla(stats['standart_sapma'])}\n"
            f"Islem Sayisi      : {stats['islem_sayisi']}"
        )
        self.analiz_metni.configure(state="normal")
        self.analiz_metni.delete("1.0", "end")
        self.analiz_metni.insert("1.0", metin)
        self.analiz_metni.configure(state="disabled")

    def _aylik_yenile(self, df):
        for satir in self.aylik_tablo.get_children():
            self.aylik_tablo.delete(satir)
        aylik = aylik_analiz(df)
        for _, satir in aylik.iterrows():
            self.aylik_tablo.insert(
                "",
                "end",
                values=(
                    satir["ay"],
                    para_formatla(satir["gelir"]),
                    para_formatla(satir["gider"]),
                    para_formatla(satir["bakiye"]),
                ),
            )

    def _grafik_fonksiyonu(self):
        from gorsellestirme import aylik_grafik, gelir_gider_bar, pasta_grafik

        secim = self.grafik_turu_var.get()
        if secim == "Toplam Bar":
            return gelir_gider_bar
        if secim == "Pasta":
            return pasta_grafik
        return aylik_grafik

    def _grafik_ciz(self):
        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except ImportError:
            messagebox.showerror("Eksik Paket", "Grafikler icin matplotlib kurulmalidir: pip install matplotlib")
            return

        for widget in self.grafik_alani.winfo_children():
            widget.destroy()
        if self.grafik_canvas:
            self.grafik_canvas = None

        df = self._veri_df()
        fig = self._grafik_fonksiyonu()(df, goster=False, kompakt=True)
        self.grafik_canvas = FigureCanvasTkAgg(fig, master=self.grafik_alani)
        self.grafik_canvas.draw()
        canvas_widget = self.grafik_canvas.get_tk_widget()
        canvas_widget.configure(height=245)
        canvas_widget.pack(fill="both", expand=True)
        self.durum_var.set(f"Grafik gosteriliyor: {self.grafik_turu_var.get()}")

    def _grafik_kaydet(self):
        dosya = filedialog.asksaveasfilename(
            title="Grafik Kaydet",
            defaultextension=".png",
            filetypes=[("PNG Dosyasi", "*.png")],
            initialdir=PROJE_KLASORU / "cikti",
            initialfile=f"{self.grafik_turu_var.get().lower().replace(' ', '_')}.png",
        )
        if not dosya:
            return
        try:
            self._grafik_fonksiyonu()(self._veri_df(), kayit_yolu=dosya, goster=False)
        except ImportError:
            messagebox.showerror("Eksik Paket", "Grafikleri kaydetmek icin matplotlib kurulmalidir.")
            return
        self.durum_var.set(f"Grafik kaydedildi: {Path(dosya).name}")


