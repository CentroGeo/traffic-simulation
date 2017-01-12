# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import colors
from sumo_utilities.simulation import count_averages, parse_types
from operator import itemgetter
from itertools import groupby
from pandas import DataFrame

matplotlib.style.use('ggplot')
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'

CONFIG = 'data/adhoc.sumocfg'
TYPES = 'data/new_types.csv'


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


def plot_windows(counts, color_list, ciclos, derivadas, zeroes):
    """ Grafica la lista de cuentas (counts) con los colores de
        la lista colors.

        La lista colors y la lista counts deben tener el mismo tamaño.
        counts: lista de las cuentas  graficar
        color_list: lista de colores para la gráfica
        ciclos: DataFrame con los ciclos de manejo para cada cuenta
        derivadas: DataFrame con las derivadas para cada ciclo de manejo
        zeroes: diccionario con los ceros de la derivada,
                calculado por zero_crosses

    """
    cmap = colors.ListedColormap(color_list)
    f, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
    smoothed[[str(i) for i in counts]].plot(ax=ax1, colormap=cmap)
    diff[[str(i) for i in counts]].plot(ax=ax2, colormap=cmap)
    ax2.axhline(y=0.05, linestyle='dashed', color='black')
    ax2.axhline(y=-0.05, linestyle='dashed', color='black')
    for i, c in enumerate(counts):
        print(cmap(i))
        ax1.axvline(x=zeroes[str(c)][0], linestyle='dashed',
                    color=cmap(i))
        ax1.axvline(x=zeroes[str(c)][3], linestyle='dashed',
                    color=cmap(i))

    plt.show()


def time_window_length(zeroes):
    """ Calcula la longitud de la ventana de tiempo para cada conteo.
        zeroes: diccionario con los ceros de la derivada,
                        calculado por zero_crosses
    """
    lengths = []
    for k, v in zeroes.items():
        if len(v) > 3:
            lengths.append((k,  v[3] - v[0]))
        else:
            lengths.append((k,  v[-1] - v[0]))
    return DataFrame(lengths)


# Leo los tipos de vehículos
types = parse_types('data/new_types.csv')
# Calculo los ciclos promedio para diferentes conteos
resultado = count_averages(types, 10, 100, 10, 80)
# Suavizo con el promedio de 5 mediciones
smoothed = resultado.rolling(10).mean()
# Calculo la derivada y la suavizo
diff = smoothed.diff(periods=3).rolling(10).mean()
# Calculo los ceros
zeroes = zero_crosses(diff, 10, 100, 10)
# Grafico para tres conteos:
graficame = [10, 50, 90]
colores = ['red', 'green', 'blue']
plot_windows(graficame, colores, smoothed, diff, zeroes)
lengths = time_window_length(zeroes)
lengths = lengths.sort_values(by=0).reset_index()
lengths[1].plot()
plt.show()
