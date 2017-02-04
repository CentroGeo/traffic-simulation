import os
import subprocess
import csv
from models.vehicle import VehicleType
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter
from xml_handlers.parsers.v_type_probe_parser import v_type_probe_parse
from xml_handlers.parsers.v_type_probe_parser import parse_output_emissions
from xml_handlers.parsers.induction_loop_parser import induction_loop_parser
from pandas import DataFrame
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'


def build_routes(count, interval, vehicle_types,
                 net='data/sumo_topes_2016.net.xml', duplicate=False):
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
                          str(interval), 'entrance', 'exit',
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
                               "--net=" + net,
                               "--output-file=" + OUT_ROUTS])
    except subprocess.CalledProcessError:
        pass  # handle errors in the called executable
    except OSError:
        pass  # executable not found
    print('routing done')


def run_simulation(config='data/cars.sumocfg', pedestrians=False,
                   emissions=False):
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

    options = ["sumo", "--configuration-file=" + config]
    if pedestrians:
        options.append("--pedestrian.model=striping")
        options.append("--fcd-output=data/output/fcd_out.xml")
        options.append("--fcd-output.geo")
        
    if emissions:
        options.append("--emission-output=data/output/emissions.xml")

    try:
        subprocess.check_call(options)
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


def count_averages(types, start_count=10, end_count=10, increment=10,
                   start_pos=10, net='data/topes_2017_simple.net.xml',
                   config='data/cars.sumocfg', pedestrians=False,
                   emissions=False, write_advisor_files=False):
    """ Regresa un DataFrame con los ciclos promedios para cada simulación
        y un diccionario con los conteos medidos (induction loop) antes del
        tope.

       Se corre una simulación para cada conteo desde start_count hasta
       end_count en incrementos de increment
       types es la lista de tipos regresada por parse_types.
    """
    car_counts = list(range(start_count, end_count, increment))
    promedios = {}
    real_counts = {}
    for cuantos in car_counts:
        build_routes(cuantos, 60, types, net=net, duplicate=True)
        run_simulation(config=config, pedestrians=pedestrians,
                       emissions=emissions)
        parsed_vehicles = v_type_probe_parse('data/output/salida.xml')
        if emissions:
            parsed_emissions = parse_output_emissions('data/output/emissions.xml')

        # Leo la salida del induction loop para saber exáctamente cuántos
        # coches pasan
        real_counts[str(cuantos)] = induction_loop_parser(
                                    'data/output/induction_out.xml')
        datos = []
        for k, v in parsed_vehicles.items():
            if 'car' in k:
                df = v.as_DataFrame()
                if emissions:
                    emissions_df = parsed_emissions[k].as_DataFrame()
                if write_advisor_files:
                    out_path = "data/output/" + str(cuantos)
                    if not os.path.exists(out_path):
                        os.makedirs(out_path)

                    f_name = out_path + "/sumo_" + k.replace('.', '_')[2:] +\
                        ".csv"
                    df.to_csv(f_name)
                    if emissions:
                        emissions_df = emissions_df.join(df, how='inner',
                                                         rsuffix='em')
                        e_name = out_path + "/emissions_" + \
                            k.replace('.', '_')[2:] + ".csv"
                        emissions_df.to_csv(e_name)

                start_index = min(df[df['position'] > start_pos].index.tolist())
                df = df[start_index:]
                df = df.reset_index(drop=True)
                datos.append(df['speed'])
        tmp_df = DataFrame(datos).transpose()
        tmp_avg = tmp_df.mean(axis=1)
        promedios[str(cuantos)] = tmp_avg

    return (DataFrame(promedios), real_counts)
