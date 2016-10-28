# -*- coding: utf-8 -*-
"""
Created on Tue May 19 11:24:35 2015
@author: plablo
"""
import argparse
import csv
import subprocess
from models.vehicle import VehicleType
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter
from sumo_utilities.driving_cycles import parse_output, write_advisor_files
# Constants
NET = 'data/topes_2015.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'


def run_simulation(count, vehicle_types):
    """Corre la simulación y escribe un csv (recorrido) por tipo de vehículo
       La simulaciòn dura una hora. Los csv que se esacriben representan los
       recorridos promedio por cada tipo de vehículo durante los segundos
       45 munutos de la simulación.
       param: count int: total de vehículos en la simulación
       param: vehicle_types list((tipo:str,accel:float,
    deccel:float,prop:float)):
               descripción de los tipos de vehículos
               por ejemplo:
               vehicle_type_proportions = [('car',0.65,0.4,0.85),
                                           ('suv',0.55,0.4,0.05),
                                           ('bus',0.45,0.3,0.05),
                                           ('microbus',0.45,0.3,0.05)]
    """
    flows = []
    for v in vehicle_types:
        v_type = VehicleType(*v[0:3])
        number = int(round(v[3] * float(count)))  # cuantos de cada tipo
        flows.append(Flow('f_' + v[0], v_type, "0",
                          "3600", '25695930#0', '-451',
                          str(number), 'max', 'free', 'best', 'max'))
    flows_writer = FlowsWriter(flows)
    flows_writer.write_xml(OUT_FLOWS)
    # call to duarouter:
    try:
        subprocess.check_call(["duarouter", "--flows=" + OUT_FLOWS,
                               "--net=" + NET,
                               "--output-file=" + OUT_ROUTS])
    except subprocess.CalledProcessError:
        pass  # handle errors in the called executable
    except OSError:
        pass  # executable not found
    print('routing done')
    try:
        subprocess.check_call(["sumo", "--configuration-file=" + CONFIG])
    except subprocess.CalledProcessError:
        pass  # handle errors in the called executable
    except OSError:
        pass  # executable not found
    print('simulation done')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Correr la simulación')
    parser.add_argument('counts',
                        help="Cantidad de vehículos en la simulación",
                        type=int)
    parser.add_argument('types_csv', help="csv con los tipos de vehículos. \
                        Lista separada por comas con los tipos y sus \
                        caracteríaticas, pej: \
                        car accel, decel, proportion, \
                        bus accel, decel, proportion. \
                        Las proporciones deben sumar 1",
                        type=str)
    parser.add_argument('--probes_file', help="Ruta al archivo con la salida \
                        del v_type_probe xml, \
                        default = data/output/salida.xml",
                        default='data/output/salida.xml', type=str)
    parser.add_argument('--out_path', help="Nombre (con path relativo) \
                        para el archivo de salida, \
                        el default es .data/output/samples.csv",
                        default='data/output/samples.csv', type=str)
    # TODO: checar argumentos: que existan los paths
    args = parser.parse_args()
# para convertir a float:

    def conv(s):
        try:
            s = float(s)
        except ValueError:
            pass
        return s
    types = []
    with open(args.types_csv) as types_csv:
        r = csv.reader(types_csv, delimiter=",", dialect=csv.excel_tab)
        # try:
        #     r = csv.reader(types_csv,delimiter=",")
        # except csv.Error:
        #     r = csv.reader(types_csv,delimiter=",",dialect=csv.excel_tab)
        for row in r:
            row = [conv(d) for d in row]
            types.append(tuple(row))
    # Llamamos a la simulación:
    run_simulation(args.counts, types)
    avg_df = parse_output()
    avg_df.to_csv('data/output/samples.csv')
    write_advisor_files()
