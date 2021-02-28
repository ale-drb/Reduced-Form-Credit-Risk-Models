import pandas as pd
import numpy as np
import ParamsCalculator as pm
import time as tm


start_time = tm.time()
# YIELD CURVE
yield_curve = pd.read_excel(r"data/yield_curve_2019.xlsx")

curve = yield_curve.iloc[:, 1:].to_numpy()
dates = yield_curve.iloc[:, 0]

t = [0.0027,
     0.08,
     0.17,
     0.25,
     0.50,
     1,
     2,
     3,
     5,
     7,
     10,
     20,
     30]

mid_time = tm.time()


yield_curve = np.array([np.array(list(zip(t, e))) for e in curve])
dated_yield_curve = dict(zip(dates, yield_curve))

end_time = tm.time()

total_time = end_time - start_time
first_run = mid_time - start_time
end_run = end_time - mid_time

# PROYECCIONES
projections = pd.read_excel(r'data/proyecciones.xlsx')
j = projections.loc[:, ['especie', 'fecha_pago', 'flow']].groupby(['especie'])

p_array = [(i, np.array(list(df.loc[:, ['fecha_pago', 'flow']
                          ].to_records(index=False)))) for i, df in j]

especies_proyecciones = dict(p_array)

# PRECIOS DE MERCADO
base = pd.read_excel(r'data\Unificada_2019_mid.xlsx',
                     sheet_name='mid_price').set_index('date')
prices = base.to_dict('index')
prices_list = list(prices.items())
subset = prices_list

# ESTIMACION
in_val = [.2, .2, .60]

h = pm.calcula_params(especies_proyecciones,
                      subset,
                      dated_yield_curve,
                      optimizer="Andritzky",
                      initial_values=in_val)

# DATAFRAME Y GUARDADO
cols = ['date', 'alpha', 'beta', 'recovery', 'fun']
df = pd.DataFrame(h, columns=cols).set_index('date')
df.to_excel(r'data/resultados_merrick_2019_midprices.xlsx')
