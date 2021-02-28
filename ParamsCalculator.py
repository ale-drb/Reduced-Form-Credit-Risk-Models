import pandas as pd
import Bonos
import Optimizador
import numpy as np


def calcula_params(cash_flows,
                   days_prices,
                   dated_curve,
                   optimizer,
                   initial_values):

    if optimizer == "Andritzky":
        optim = Optimizador.AndritzkyOptimizer
    else:
        optim = Optimizador.MerrickOptimizer

    estimation_list = []
    # estimation_array = np.array([])

    for a, b in days_prices:

        if a in dated_curve:
            print(a)
            cartera = np.array([Bonos.Bono(k, b[k], cash_flows[k], a)
                               for k in cash_flows])
            opt = optim(cartera, dated_curve[a], initial_values)
            estimations = opt.optimize()
            est_list = list(estimations)
            est_list.insert(0, a)
            # est_array = np.insert(estimations, 0, a)
            estimation_list.append(tuple(est_list))
            # np.append(estimation_array, tuple(est_array))

    return estimation_list
    # return estimation_array
