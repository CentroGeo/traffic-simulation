import os
import subprocess
import csv
from models.vehicle import VehicleType
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'


def build_routes(count, interval, vehicle_types, duplicate=False):
    """Escribe el arcivo de flujos y el de rutas.
       param: count int: total de vehículos en la simulación
       param: interval int: Duración de la simulación
       param: vehicle_types list((tipo:str,accel:float,
                                  deccel:float,prop:float)):
               descripción de los tipos de vehículos
               por ejemplo:
               vehicle_type_proportions = [('car',0.65,0.4,0.85),
                                           ('suv',0.55,0.4,0.05),
                                           ('bus',0.45,0.3,0.05),
                                           ('microbus',0.45,0.3,0.05)]
       param: duplicate bool: Si es True entonces se duplica el intervalo y
                              la cuenta de vehículos
    """
    flows = []
    if duplicate:
        interval = 2*interval
        count = 2*count
    for v in vehicle_types:
        v_type = VehicleType(*v[0:3])
        number = int(round(v[3] * float(count)))  # cuantos de cada tipo
        flows.append(Flow('f_' + v[0], v_type, "0",
                          str(interval), '-32995#0', '-32995#2.389.456',
                          str(number), 'max', 'free', 'best', 'max'))
    flows_writer = FlowsWriter(flows)
    flows_writer.write_xml(OUT_FLOWS)
    # borrar las rutas anteriores antes de escribir las nuevas:
    try:
        os.remove(OUT_ROUTS)
    except:
        pass

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


def run_simulation():
    """Corre la simulación utilizando la configuración de data/adhoc.sumocfg.

       Los flujos siempre van a ser data/hourly_flows.xml y las rutas
       data/routes.rou.xml.

       Escribe el archivo data/output/salida.xml con los resultados de
       los v_type_probes
    """

    # Elimino el archivo de salida:
    try:
        os.remove('data/output/salida.xml')
    except:
        pass

    try:
        subprocess.check_call(["sumo", "--configuration-file=" + CONFIG])
    except subprocess.CalledProcessError:
        pass  # handle errors in the called executable
    except OSError:
        pass  # executable not found
    print('simulation done')


def parse_types(types_file):
    def conv(s):
        try:
            s = float(s)
        except ValueError:
            pass
        return s

    types = []
    with open(types_file) as types_csv:
        r = csv.reader(types_csv, delimiter=",", dialect=csv.excel_tab)
        for row in r:
            row = [conv(d) for d in row]
            types.append(tuple(row))
    return types
