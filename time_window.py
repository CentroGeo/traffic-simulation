# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
from pandas import DataFrame
from sumo_utilities.simulation import cycle_averages, parse_types
from sumo_utilities.time_window import zero_crosses, plot_windows
from sumo_utilities.time_window import time_window_length
matplotlib.style.use('ggplot')
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'

CONFIG = 'data/adhoc.sumocfg'
TYPES = 'data/new_types.csv'


# Leo los tipos de vehículos
types = parse_types('data/new_types.csv')
# Calculo los ciclos promedio para diferentes conteos
resultado, emisiones, real_counts = cycle_averages(types, 10, 100, 10, 80)
# Procesamos los real_counts para producir un DataFrame por cada
# count original
counts_dict = {}
for k, v in real_counts.items():
    tmp_df = DataFrame.from_dict(v, orient='index')
    tmp_df.index = tmp_df.index.map(float)
    tmp_df.index = tmp_df.index.map(int)
    tmp_df = tmp_df.sort_index()
    counts_dict[k] = tmp_df

# Suavizo los ciclos promedio con el promedio de 10 mediciones
smoothed = resultado.rolling(10).mean()
# Calculo la derivada y la suavizo
diff = smoothed.diff(periods=3).rolling(10).mean()
# Calculo los ceros
zeroes = zero_crosses(diff, 10, 100, 10)
# Grafico los ciclos promedio para tres conteos y sus respectivos
# conteos reales:
graficame = [10, 50, 90]
colores = ['red', 'green', 'blue']
plot_windows(graficame, colores, smoothed, diff, counts_dict, zeroes)
lengths = time_window_length(zeroes)
lengths = lengths.sort_values(by=0).reset_index()
lengths[1].plot()
plt.show()
