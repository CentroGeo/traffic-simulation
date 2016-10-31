import subprocess
from models.vehicle import VehicleType
from models.flow import Flow
from xml_handlers.writers.flows_writer import FlowsWriter
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'


def run_simulation(count, interval, vehicle_types):
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
                          str(interval), '-32995#0', '-32995#2.389.456',
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
