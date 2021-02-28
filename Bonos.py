import pandas as pd


class Bono():
    """
    Crea un Bono.
    Parámetros:
        especie     : Código de Negociación del Instrumento
        price       : Precio de Mercado del Instrumento.
        cash_flows  : Lista de tuplas (fecha, cash flow).
        price_date  : Fecha del precio del bono.
    """
    def __init__(self, especie, price, cash_flows, price_date):
        self.__type = 'Bono'
        self.__name = especie
        self._price = price
        self._cash_flows = cash_flows
        self._price_date = price_date

    def __repr__(self):
        return f'{self.__name} @ {self._price}'

    def year_fracc(self, d1, d2):
        d1 = pd.to_datetime(d1)
        months = (d1.year - d2.year) * 12 + d1.month - d2.month
        days = (d1 - d2).days - months * 30
        year_fracc = (months * 30 + days)/360

        return year_fracc

    def gen_cash_flows(self):

        return [(self.year_fracc(t, self._price_date), flow) for t, flow in
                self._cash_flows if self.year_fracc(t, self._price_date) > 0]

    def gen_pagos(self):
        """
        Genera el Flujo de Pagos del Instrumento.
        """
        if any(self._cash_flows):
            cf = self.gen_cash_flows()
        else:
            pass

        return cf
