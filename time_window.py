# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
from sumo_utilities.simulation import count_averages, parse_types
from operator import itemgetter
from itertools import groupby

matplotlib.style.use('ggplot')
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'

CONFIG = 'data/adhoc.sumocfg'
TYPES = 'data/new_types.csv'

types = parse_types('data/new_types.csv')
# Calculo los ciclos promedio para diferentes conteos
resultado = count_averages(types, 10, 100, 10, 80)

# Suavizo con el promedio de 5 mediciones
smoothed = resultado.rolling(10).mean()

# Calculo la derivada y la suavizo
diff = smoothed.diff(periods=3).rolling(5).mean()
# diff = smoothed.diff(periods=3)

f, axarr = plt.subplots(4, sharex=True)
smoothed.plot(ax=axarr[0])
diff.plot(ax=axarr[1])
plt.axhline(y=0.1, linestyle='dashed', color='black')
plt.axhline(y=-0.1, linestyle='dashed', color='black')
pct_change_diff = diff.pct_change(periods=3)
pct_change_diff.plot(ax=axarr[2])
pct_change_sm = smoothed.pct_change(periods=3)
pct_change_sm.plot(ax=axarr[3])
plt.show()

f, axarr = plt.subplots(2, sharex=True)
smoothed[['10', '50']].plot(ax=axarr[0])
diff[['10', '50']].plot(ax=axarr[1])
# pct_change_diff = diff[['10', '50', '90']].pct_change(periods=1)
# pct_change_diff.plot(ax=axarr[2])
plt.axhline(y=0.1, linestyle='dashed', color='black')
plt.axhline(y=-0.1, linestyle='dashed', color='black')
plt.axhline(y=0.05, linestyle='dashed', color='red')
plt.axhline(y=-0.05, linestyle='dashed', color='red')
plt.show()

#Hafcemos una lista de los índices dónde la derivada es mayor que cero:
greater_10 = diff[abs(diff['10']) >= 0.05].index.tolist()

# Partimos la lista de mayores de cero en  pedazos consecutivos
chunks = []
for k, g in groupby(enumerate(greater_10), lambda x:x[0] - x[1]):
    chunks.append(list(map(itemgetter(1), g)))

# Tomamos el primer elemento de cada chunk, esos son los cruces en cero:
zero_cross = []
for l in chunks:
    zero_cross.append(l[0])

print(zero_cross)
