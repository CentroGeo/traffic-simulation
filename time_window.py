# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import colors
import matplotlib.gridspec as gridspec
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


def plot_windows(counts, color_list, ciclos, derivadas, real_counts, zeroes):
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
    fig = plt.figure(1)
    cmap = colors.ListedColormap(color_list)
    grid_rows = len(counts)
    gs = gridspec.GridSpec(grid_rows + 1, 2, width_ratios=[3, 5])
    ax2 = plt.subplot(gs[2:grid_rows + 1, 1])
    ax1 = plt.subplot(gs[0:2, 1])
    ax1.set_title('Ciclos Promedio')
    ax2.set_title('Aceleraciones')
    smoothed[[str(i) for i in counts]].plot(ax=ax1, colormap=cmap)
    diff[[str(i) for i in counts]].plot(ax=ax2, colormap=cmap)
    ax2.axhline(y=0.05, linestyle='dashed', color='black')
    ax2.axhline(y=-0.05, linestyle='dashed', color='black')
    ax2.set_xlabel('Tiempo')
    ax1.set_ylabel('Velocidad')
    ax2.set_ylabel('Aceleración')
    # plt.tight_layout()
    for i, c in enumerate(counts):
        ax1.axvline(x=zeroes[str(c)][0], linestyle='dashed',
                    color=cmap(i))
        ax1.axvline(x=zeroes[str(c)][3], linestyle='dashed',
                    color=cmap(i))
        if i == 0:
            bar_ax = plt.subplot(gs[i, 0])
            bar_ax.set_title('Conteos medidos')
        else:
            bar_ax = plt.subplot(gs[i, 0], sharex=bar_ax)
        bar_ax.set_xlabel('Tiempo')
        bar_ax.set_ylabel('Conteo')
        real_counts[str(c)].plot.bar(ax=bar_ax, color=cmap(i), legend=False)
    gs.tight_layout(fig)
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
resultado, real_counts = count_averages(types, 10, 100, 10, 80)
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
