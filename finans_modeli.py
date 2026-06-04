"""Finans uygulamasinin nesne tabanli veri modeli."""

from __future__ import annotations

from datetime import datetime


class Islem:
    """Gelir veya gider kaydini temsil eden sinif."""

    GECERLI_TIPLER = {"gelir", "gider"}

    def __init__(self, id, tutar, tarih, aciklama, tip):
        """
        id: int
        tutar: float
        tarih: str (YYYY-MM-DD)
        aciklama: str
        tip: 'gelir' veya 'gider'
        """
        self.id = int(id)
        self.tutar = self._tutar_dogrula(tutar)
        self.tarih = self._tarih_dogrula(tarih)
        self.aciklama = str(aciklama).strip() or "Aciklama yok"
        self.tip = self._tip_dogrula(tip)

    @staticmethod
    def _tutar_dogrula(tutar):
        tutar = float(tutar)
        if tutar <= 0:
            raise ValueError("Tutar 0'dan buyuk olmalidir.")
        return tutar

    @staticmethod
    def _tarih_dogrula(tarih):
        tarih = str(tarih).strip()
        try:
            datetime.strptime(tarih, "%Y-%m-%d")
        except ValueError as hata:
            raise ValueError("Tarih formati YYYY-MM-DD olmalidir.") from hata
        return tarih

    @classmethod
    def _tip_dogrula(cls, tip):
        tip = str(tip).strip().lower()
        if tip not in cls.GECERLI_TIPLER:
            raise ValueError("Tip 'gelir' veya 'gider' olmalidir.")
        return tip

    def to_dict(self):
        """Islem nesnesini CSV ve DataFrame icin sozluge donusturur."""
        return {
            "id": self.id,
            "tutar": self.tutar,
            "tarih": self.tarih,
            "aciklama": self.aciklama,
            "tip": self.tip,
        }

    @classmethod
    def from_dict(cls, veri):
        """CSV satirindan Islem nesnesi olusturur."""
        return cls(
            veri["id"],
            veri["tutar"],
            veri["tarih"],
            veri["aciklama"],
            veri["tip"],
        )

    def ozet_satir(self):
        """Listeleme ekranlari icin okunabilir metin uretir."""
        isaret = "+" if self.tip == "gelir" else "-"
        return f"{self.id:>3} | {self.tarih} | {self.tip:<5} | {isaret}{self.tutar:>10.2f} TL | {self.aciklama}"

    def __repr__(self):
        return (
            f"Islem(id={self.id}, tutar={self.tutar}, tarih='{self.tarih}', "
            f"aciklama='{self.aciklama}', tip='{self.tip}')"
        )
