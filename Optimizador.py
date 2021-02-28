import scipy.optimize as sco
import Bonos
from numpy import exp, sqrt, append, sum


class MerrickOptimizer:

    def __init__(self, bonds_list, yield_curve, initial_values):
        self._bonds_list = bonds_list
        self._yc = yield_curve
        self._initial_values = initial_values

    def interpola_tasa(self, plazo_obj):
        """
        Realiza interpolación lineal de tasas a partir de datos de mercado.
        Parámetros:
            curva     : Lista de tuplas (plazo, tasa) ordenada por plazo.
            plazo_obj : Plazo para el cual se desea calcular la tasa.
        """
        if plazo_obj < self._yc[0][0] or plazo_obj > self._yc[-1][0]:
            raise RuntimeError('Plazo objetivo fuera de los datos de la curva')

        ind_prox = sum(1 for a, b in self._yc if a < plazo_obj)

        if plazo_obj == self._yc[ind_prox][0]:
            return self._yc[ind_prox][1]

        prev, prox = self._yc[ind_prox - 1], self._yc[ind_prox]

        diff_tasa = prox[1] - prev[1]
        diff_plazo = prox[0] - prev[0]

        return prev[1] + (plazo_obj - prev[0]) / diff_plazo * diff_tasa

    def optimize(self):

        def npv(p, price, pagos):
            diff = price - sum(exp(- p[0]*t - p[1] * (1 - exp(-t))) * f *
                               exp(-self.interpola_tasa(t) * t)
                               + (exp(- p[0] * (t - .5) - p[1] *
                                      (1 - exp(-t + .5)))
                               - exp(-p[0]*t - p[1]*(1-exp(-t)))) *
                               exp(-self.interpola_tasa(t) * t) * p[2] * 100
                               for t, f in pagos)

            return diff

        def ssr(p):
            return sum(npv(p, e._price, e.gen_pagos()) ** 2
                       for e in self._bonds_list)

        bnds = ((None, None), (None, None), (0, None))

        def constraint_1(p):
            n = float(len(self._bonds_list))

            return sum(npv(p, e._price, e.gen_pagos())
                       for e in self._bonds_list)/n

        def constraint_2(p):
            delta = p[0] + p[1] * (1 - exp(-10))/10

            return 1 - exp(- 10 * delta)

        cons = ({'type': 'eq',
                'fun': constraint_1},
                {'type': 'ineq',
                'fun': constraint_2})

        result = sco.minimize(ssr,
                              self._initial_values,
                              bounds=bnds,
                              constraints=cons)

        return append(result.x, result.fun)


class AndritzkyOptimizer:

    def __init__(self, bonds_list, yield_curve, initial_values):
        self._bonds_list = bonds_list
        self._yc = yield_curve
        self._initial_values = initial_values

    def interpola_tasa(self, plazo_obj):
        """
        Realiza interpolación lineal de tasas a partir de datos de mercado.
        Parámetros:
            curva     : Lista de tuplas (plazo, tasa) ordenada por plazo.
            plazo_obj : Plazo para el cual se desea calcular la tasa.
        """
        if plazo_obj < self._yc[0][0] or plazo_obj > self._yc[-1][0]:
            raise RuntimeError('Plazo objetivo fuera de los datos de la curva')

        ind_prox = sum(1 for a, b in self._yc if a < plazo_obj)

        if plazo_obj == self._yc[ind_prox][0]:
            return self._yc[ind_prox][1]

        prev, prox = self._yc[ind_prox - 1], self._yc[ind_prox]

        diff_tasa = prox[1] - prev[1]
        diff_plazo = prox[0] - prev[0]

        return prev[1] + (plazo_obj - prev[0]) / diff_plazo * diff_tasa

    def optimize(self):
        def npv(p, price, pagos):
            # rf = .01

            diff = price - sum((1 - exp(- exp((p[0] - t)/p[1]))) * f *
                               exp(- self.interpola_tasa(t) * t)
                               + (exp(- exp((p[0] - t)/p[1])) -
                                  exp(- exp((p[0] - t + .5)/p[1]))) *
                               exp(- self.interpola_tasa(t) * t) * p[2] * 100
                               for t, f in pagos)

            return diff/price

        def rmse(p):

            n = float(len(self._bonds_list))

            return sqrt(sum(npv(p, e._price, e.gen_pagos())**2
                            for e in self._bonds_list)/n)

        bnds = ((0, None), (0, None), (0, None))

        result = sco.minimize(rmse,
                              self._initial_values,
                              bounds=bnds)

        return append(result.x, result.fun)
