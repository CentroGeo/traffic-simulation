# -*- coding: utf-8 -*-
"""
Created on Tue May 19 11:24:35 2015
@author: plablo
"""
import argparse
from sumo_utilities.driving_cycles import parse_output, write_advisor_files
from sumo_utilities.simulation import build_routes, run_simulation, parse_types
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Correr la simulación')
    parser.add_argument('counts',
                        help="Cantidad de vehículos en la simulación",
                        type=int, default=10)
    parser.add_argument('interval',
                        help="Duración de la simulación en segundos",
                        type=int, default=30)

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
    # Parseamos el archivo con los tipos.
    types = parse_types(args.types_csv)
    # Llamamos a la simulación:
    build_routes(args.counts, args.interval, types)
    run_simulation()
    avg_df = parse_output()
    avg_df.to_csv('data/output/samples.csv')
    write_advisor_files()
