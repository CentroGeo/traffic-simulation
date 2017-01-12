# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import colors
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
diff = smoothed.diff(periods=3).rolling(10).mean()
# diff = smoothed.diff(periods=3)

# Función para obtener los cruces en cero:


def zero_crosses(diff, start, end, increment):
    zeros = {}
    for count in range(start, end, increment):
        # Hacemos una lista de los índices dónde la derivada es mayor que cero:
        greater_0 = diff[abs(diff[str(count)]) >= 0.05].index.tolist()    
        # Partimos la lista de mayores de cero en  pedazos consecutivos
        chunks = []
        for k, g in groupby(enumerate(greater_0), lambda x: x[0] - x[1]):
            chunks.append(list(map(itemgetter(1), g)))
        zeros[str(count)] = chunks

    # Para cada lista, tomamos el primer elemento de cada chunk,
    # esos son los cruces en cero:
    zero_crosses = {}
    for k, v in zeros.items():
        this_count = []
        for l in v:
            this_count.append(l[0])
        zero_crosses[k] = this_count

    return zero_crosses


zeroes = zero_crosses(diff, 10, 100, 10)
print(zeroes)


cmap = colors.ListedColormap(['red', 'green', 'blue'])
f, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
smoothed[['10', '50', '90']].plot(ax=ax1, colormap=cmap)
diff[['10', '50', '90']].plot(ax=ax2, colormap=cmap)
ax2.axhline(y=0.05, linestyle='dashed', color='black')
ax2.axhline(y=-0.05, linestyle='dashed', color='black')
ax1.axvline(x=zeroes['10'][0], linestyle='dashed', color='red')
ax1.axvline(x=zeroes['10'][3], linestyle='dashed', color='red')
ax1.axvline(x=zeroes['50'][0], linestyle='dashed', color='green')
ax1.axvline(x=zeroes['50'][3], linestyle='dashed', color='green')
ax1.axvline(x=zeroes['90'][0], linestyle='dashed', color='blue')
ax1.axvline(x=zeroes['90'][3], linestyle='dashed', color='blue')
plt.show()
