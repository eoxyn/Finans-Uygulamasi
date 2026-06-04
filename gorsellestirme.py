"""Matplotlib ile finansal grafik olusturma fonksiyonlari."""

from __future__ import annotations

from pathlib import Path

from analiz import aylik_analiz, toplam_gelir_gider


RENKLER = {
    "gelir": "#15803d",
    "gider": "#b91c1c",
    "bakiye": "#2563eb",
    "zemin": "#ffffff",
    "panel": "#f8fafc",
    "metin": "#0f172a",
    "izgara": "#dbe3ef",
}


def _matplotlib_hazirla():
    import matplotlib.pyplot as plt

    try:
        import seaborn as sns

        sns.set_theme(style="darkgrid")
    except ImportError:
        plt.style.use("ggplot")
    return plt


def _kaydet(fig, kayit_yolu):
    if kayit_yolu:
        yol = Path(kayit_yolu)
        yol.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(yol, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
        return yol
    return None


def aylik_grafik(df, kayit_yolu=None, goster=True, kompakt=False):
    """Aylik gelir ve giderleri karsilastiran cizgi grafigi olusturur."""
    plt = _matplotlib_hazirla()
    aylik = aylik_analiz(df)
    fig_boyutu = (6.7, 2.9) if kompakt else (10, 5)
    fig, ax = plt.subplots(figsize=fig_boyutu, facecolor=RENKLER["zemin"])
    ax.set_facecolor(RENKLER["panel"])

    if aylik.empty:
        ax.text(0.5, 0.5, "Grafik icin veri yok", ha="center", va="center", color=RENKLER["metin"])
    else:
        ax.plot(aylik["ay"], aylik["gelir"], marker="o", linewidth=2.5, color=RENKLER["gelir"], label="Gelir")
        ax.plot(aylik["ay"], aylik["gider"], marker="o", linewidth=2.5, color=RENKLER["gider"], label="Gider")
        ax.plot(aylik["ay"], aylik["bakiye"], marker="o", linewidth=2.0, color=RENKLER["bakiye"], label="Bakiye")
        ax.legend()

    baslik_boyutu = 12 if kompakt else 15
    ax.set_title("Aylik Gelir-Gider Analizi", color=RENKLER["metin"], fontsize=baslik_boyutu, weight="bold", pad=8)
    ax.set_xlabel("Ay", color=RENKLER["metin"])
    ax.set_ylabel("Tutar (TL)", color=RENKLER["metin"])
    ax.tick_params(colors=RENKLER["metin"])
    ax.grid(color=RENKLER["izgara"], linewidth=1)
    if kompakt:
        fig.subplots_adjust(top=0.83, bottom=0.23, left=0.12, right=0.98)
    else:
        fig.tight_layout()
    _kaydet(fig, kayit_yolu)
    if goster:
        plt.show()
    return fig


def gelir_gider_bar(df, kayit_yolu=None, goster=True, kompakt=False):
    """Toplam gelir ve gider degerlerini karsilastiran sutun grafigi olusturur."""
    plt = _matplotlib_hazirla()
    ozet = toplam_gelir_gider(df)
    fig_boyutu = (6.7, 2.9) if kompakt else (8, 5)
    fig, ax = plt.subplots(figsize=fig_boyutu, facecolor=RENKLER["zemin"])
    ax.set_facecolor(RENKLER["panel"])
    etiketler = ["Gelir", "Gider", "Bakiye"]
    degerler = [ozet["toplam_gelir"], ozet["toplam_gider"], ozet["bakiye"]]
    renkler = [RENKLER["gelir"], RENKLER["gider"], RENKLER["bakiye"]]
    ax.bar(etiketler, degerler, color=renkler, width=0.58)
    baslik_boyutu = 12 if kompakt else 15
    ax.set_title("Toplam Finans Ozeti", color=RENKLER["metin"], fontsize=baslik_boyutu, weight="bold", pad=8)
    ax.set_ylabel("Tutar (TL)", color=RENKLER["metin"])
    ax.tick_params(colors=RENKLER["metin"])
    ax.grid(axis="y", color=RENKLER["izgara"], linewidth=1)
    if kompakt:
        fig.subplots_adjust(top=0.83, bottom=0.18, left=0.13, right=0.98)
    else:
        fig.tight_layout()
    _kaydet(fig, kayit_yolu)
    if goster:
        plt.show()
    return fig


def pasta_grafik(df, kayit_yolu=None, goster=True, kompakt=False):
    """Gelir ve gider oranlarini gosteren pasta grafigi olusturur."""
    plt = _matplotlib_hazirla()
    ozet = toplam_gelir_gider(df)
    fig_boyutu = (5.6, 3.7) if kompakt else (7.4, 6.2)
    fig, ax = plt.subplots(figsize=fig_boyutu, facecolor=RENKLER["zemin"])
    degerler = [ozet["toplam_gelir"], ozet["toplam_gider"]]

    if sum(degerler) == 0:
        ax.text(0.5, 0.5, "Grafik icin veri yok", ha="center", va="center", color=RENKLER["metin"])
    else:
        wedges, etiket_yazilari, yuzde_yazilari = ax.pie(
            degerler,
            labels=["Gelir", "Gider"],
            autopct="%1.1f%%",
            startangle=90,
            radius=1.0,
            pctdistance=0.6,
            labeldistance=1.1,
            colors=[RENKLER["gelir"], RENKLER["gider"]],
            wedgeprops={"linewidth": 2, "edgecolor": RENKLER["zemin"]},
            textprops={"color": RENKLER["metin"], "weight": "bold"},
        )
        etiket_boyutu = 11 if kompakt else 14
        yuzde_boyutu = 10 if kompakt else 13
        for yazi in etiket_yazilari:
            yazi.set_fontsize(etiket_boyutu)
        for yazi in yuzde_yazilari:
            yazi.set_fontsize(yuzde_boyutu)
            yazi.set_color(RENKLER["zemin"])
    baslik_boyutu = 12 if kompakt else 15
    ax.set_title("Gelir-Gider Orani", color=RENKLER["metin"], fontsize=baslik_boyutu, weight="bold", pad=10)
    ax.set_aspect("equal")
    if kompakt:
        fig.subplots_adjust(top=0.9, bottom=0.03, left=0.02, right=0.98)
    else:
        fig.subplots_adjust(top=0.9, bottom=0.03, left=0.03, right=0.97)
    _kaydet(fig, kayit_yolu)
    if goster:
        plt.show()
    return fig
