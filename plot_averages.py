# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import axes3d
import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from xml_handlers.parsers.v_type_probe_parser import v_type_probe_parse


def average_output(probe_file='data/output/salida.xml',
                   output_file='data/output/averaged_samples.csv',
                   time_intervals=10,
                   length_intervals=200):
    """Lee el vtype_probe resultado de una simulación y escribe un csv con
       las velocidades promedio para cada intervalo (espacio-temporal)
       muestreado.

       param: probe_file str: path al xml de salida de un vtype_probe
       param: output_file str: path del csv de salida param:
       time_intervals int: número de intervalos de tiempo a usar
       param: length_intervals int: número de intervalos de longitud a
       usar

    """

    parsed_vehicles = v_type_probe_parse(probe_file)
    print('Datos de la simulación')
    print('total de vehiculos: ' + str(len(parsed_vehicles)))
    timesteps = []
    positions = []
    for k, v in parsed_vehicles.items():
        timesteps.extend(v.timesteps)
        positions.extend([c[2] for c in v.driving_cycle])
    min_pos = min(positions)
    max_pos = max(positions)
    length_window = (max_pos - min_pos)/length_intervals
    timesteps = sorted(list(set(timesteps)))
    min_time = min(timesteps)
    max_time = max(timesteps)
    time_window = (max_time - min_time)/time_intervals
    print('intervalos muestreados: ' + str(len(timesteps)))
    print('posición mínima: ' + str(min_pos))
    print('posición máxima: ' + str(max_pos))
    print('longitud de muestreo: ' + str(length_window))
    print('timsteps: ' + str(max_time))
    length_intervals_list = [min_pos + k*length_window for k in
                             range(0, length_intervals+1)]

    time_intervals_list = [min_time + k*time_window
                           for k in range(0, time_intervals+1)]
    # Sample positions

    positions_sample = []
    for i in range(0, len(length_intervals_list) - 1):
        positions_sample.append([])
        for k, v in parsed_vehicles.items():
            for step in v.driving_cycle:
                if (step[2] >= length_intervals_list[i] and
                        step[2] <= length_intervals_list[i + 1]):
                    positions_sample[i].append(step)

    # Time samples
    samples = []
    suma = 0
    v_cnt = 0
    for i, length_sample in enumerate(positions_sample):
        samples.append([])
        for t in range(0, len(time_intervals_list) - 1):
            for v in length_sample:
                if (v[0] >= time_intervals_list[t] and
                        v[0] <= time_intervals_list[t + 1]):
                    suma += v[3]
                    v_cnt += 1
            if v_cnt != 0:
                samples[i].append(suma / v_cnt)
            else:
                pass
            suma = 0
            v_cnt = 0
    return samples


def build_plots(samples):
    """Toma las muestras espacio-temporaes y produce la gráfica."""

    data = samples
    x_len = len(data[0])
    y_len = len(data)
    X, Y = np.meshgrid([i for i in range(0, x_len)],
                       [i for i in range(0, y_len)])
    Z = []
    for i, row in enumerate(data):
        Z.append([])
        for e in row:
            try:
                Z[i].append(float(e))
            except:
                print(e)
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(X, Y, np.array(Z))

    Z_array = np.array(Z)
    Z_array = np.transpose(Z_array)

    fig_2 = plt.figure(2)
    ax_2 = fig_2.add_subplot(111, projection='3d')
    cmap = cm.get_cmap("jet", 3*x_len)
    cvals = cmap(np.arange(3*x_len))
    for z in [i for i in range(0, x_len)]:
        xs = np.arange(y_len)
        ys = Z_array[z, :]
        print(cvals[z, :])
        ax_2.bar(xs, ys, zs=z, zdir='y', color=cvals[z*3, :],
                 linewidth=0, alpha=0.8)
    ax_2.set_xlabel('Distancia')
    ax_2.set_ylabel('Tiempo')
    ax_2.set_zlabel('Velocidad')

    plt.show()


if __name__ == '__main__':
    samples = average_output()
    build_plots(samples)
