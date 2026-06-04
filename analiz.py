"""Pandas ve NumPy ile finansal analiz fonksiyonlari."""

from __future__ import annotations

import numpy as np
import pandas as pd


DF_KOLONLARI = ["id", "tutar", "tarih", "aciklama", "tip"]


def verileri_dataframe_yap(gelirler, giderler):
    """Gelir ve gider listelerini birlestirerek pandas DataFrame'e donusturur."""
    kayitlar = [islem.to_dict() for islem in gelirler + giderler]
    df = pd.DataFrame(kayitlar, columns=DF_KOLONLARI)

    if df.empty:
        df["tutar"] = pd.Series(dtype="float")
        df["tarih"] = pd.Series(dtype="datetime64[ns]")
        df["tip"] = pd.Series(dtype="str")
        return df

    df["tutar"] = pd.to_numeric(df["tutar"], errors="coerce").fillna(0.0)
    df["tarih"] = pd.to_datetime(df["tarih"], errors="coerce")
    df = df.dropna(subset=["tarih"]).sort_values(["tarih", "id"]).reset_index(drop=True)
    return df


def toplam_gelir_gider(df):
    """DataFrame uzerinden toplam gelir, gider ve bakiyeyi hesaplar."""
    if df.empty:
        return {"toplam_gelir": 0.0, "toplam_gider": 0.0, "bakiye": 0.0}

    toplam_gelir = float(df.loc[df["tip"] == "gelir", "tutar"].sum())
    toplam_gider = float(df.loc[df["tip"] == "gider", "tutar"].sum())
    return {
        "toplam_gelir": toplam_gelir,
        "toplam_gider": toplam_gider,
        "bakiye": toplam_gelir - toplam_gider,
    }


def aylik_analiz(df):
    """Verileri aylik bazda gelir, gider ve bakiye olarak ozetler."""
    if df.empty:
        return pd.DataFrame(columns=["ay", "gelir", "gider", "bakiye"])

    aylik_df = df.copy()
    aylik_df["ay"] = aylik_df["tarih"].dt.to_period("M").astype(str)
    pivot = (
        aylik_df.pivot_table(index="ay", columns="tip", values="tutar", aggfunc="sum")
        .fillna(0.0)
        .reset_index()
    )

    for kolon in ("gelir", "gider"):
        if kolon not in pivot.columns:
            pivot[kolon] = 0.0

    pivot["bakiye"] = pivot["gelir"] - pivot["gider"]
    return pivot[["ay", "gelir", "gider", "bakiye"]]


def numpy_istatistik(df):
    """NumPy kullanarak ortalama, minimum, maksimum ve standart sapma hesaplar."""
    if df.empty:
        return {
            "ortalama": 0.0,
            "minimum": 0.0,
            "maksimum": 0.0,
            "standart_sapma": 0.0,
            "islem_sayisi": 0,
        }

    tutarlar = df["tutar"].to_numpy(dtype=float)
    return {
        "ortalama": float(np.mean(tutarlar)),
        "minimum": float(np.min(tutarlar)),
        "maksimum": float(np.max(tutarlar)),
        "standart_sapma": float(np.std(tutarlar)),
        "islem_sayisi": int(tutarlar.size),
    }
