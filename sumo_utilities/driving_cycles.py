# -*- coding: utf-8 -*-
import csv
from pandas import DataFrame
from xml_handlers.parsers.v_type_probe_parser import v_type_probe_parse


def parse_output(probe_file='data/output/salida.xml'):
    """Lee el vtype_probe resultado de una simulación y escribe un csv por
       cada tipo de vehículo con los ciclos de manejo promedio. La resolución
       espacial del ciclo está determinada por el parámetro delta (metros).

       param: probe_file str: path al xml de salida de un vtype_probe
       param: output_path str: path en donde se guardan los csvs
    """

    parsed_vehicles = v_type_probe_parse(probe_file)
    print('Datos de la simulación')
    print('total de vehiculos: ' + str(len(parsed_vehicles)))

    # Encontramos los tipos de vehículos:
    types = []
    for c in parsed_vehicles.keys():
        t = c.split(".")[0]
        t = t.split("_")[1]
        types.append(t)
        data = {}

    types = set(types)
    data = {}
    for t in types:
        data[t] = {}
        for k, v in parsed_vehicles.items():
            if t in v.id:
                data[t][v.id] = [float(s) for s in v.speeds]

    # Cortamos con el menor tiempo de recorrido para cada tipo:
    for k, v in data.items():
        min_time = min([len(l) for k, l in v.items()])
        for a, b in v.items():
            v[a] = b[:min_time]

    # Creamos un DataFrame por cada tipo, promediamos sobre los vehículos,
    # hacemos un DataFrame con los promedios por tipo y exportamos como csv:

    series = {}
    for v_type, cycle in data.items():
        df = DataFrame(cycle)
        series[v_type] = df.mean(axis=1)

    avg_df = DataFrame(series)
    avg_df.index.name = 'tiempo'
    return avg_df


def write_advisor_files(probe_file='data/output/salida.xml',
                        output_path='data/output/'):

    parsed_vehicles = v_type_probe_parse(probe_file)
    for k, v in parsed_vehicles.items():
        v_name = k.replace('.', '_')[2:]
        with open(output_path + "sumo_" + v_name + ".csv", "w") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['t_global', 't_vehiculo', 'velocidad',
                                'carril',  'x', 'y', 'distancia'])
            for j, t in enumerate(v.timesteps):
                renglon = [t, j, v.speeds[j], v.lanes[j].split('_').pop(),
                           v.coordinates[j][0], v.coordinates[j][1],
                           v.positions[j]]
                spamwriter.writerow(renglon)
