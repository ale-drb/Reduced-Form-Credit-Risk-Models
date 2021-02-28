import pandas as pd
import numpy as np
import ParamsCalculator as pm
import time as tm


start_time = tm.time()
# YIELD CURVE
yield_curve = pd.read_excel(INSERT FILE PATH FOR YIELD CURVE)

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

# CASH FLOWS
projections = pd.read_excel(INSERT FILE PATH FOR CASH FLOWS)
j = projections.loc[:, ['especie', 'fecha_pago', 'flow']].groupby(['especie'])

p_array = [(i, np.array(list(df.loc[:, ['fecha_pago', 'flow']
                          ].to_records(index=False)))) for i, df in j]

especies_proyecciones = dict(p_array)

# MARKET PRICES
base = pd.read_excel(INSERT FILE PATH FOR MARKET PRICES,
                     sheet_name='mid_price').set_index('date')
prices = base.to_dict('index')
prices_list = list(prices.items())
subset = prices_list

# ESTIMATION
in_val = [1, 2, .60]

h = pm.calcula_params(especies_proyecciones,
                      subset,
                      dated_yield_curve,
                      optimizer="Andritzky",
                      initial_values=in_val)

# OUTPUT AND SAVING
cols = ['date', 'alpha', 'beta', 'recovery', 'fun']
df = pd.DataFrame(h, columns=cols).set_index('date')
df.to_excel(INSERT PATH FOR OUTPUT)
