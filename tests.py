# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from pandas import DataFrame
import pandas as pd
from sumo_utilities.simulation import build_routes, run_simulation, parse_types
from sumo_utilities.driving_cycles import time_average
from sumo_utilities.driving_cycles import write_advisor_files
from xml_handlers.parsers.v_type_probe_parser import v_type_probe_parse

matplotlib.style.use('ggplot')
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'
TYPES = 'data/new_types.csv'

types = parse_types('data/new_types.csv')
resultados_time = []
#resultados_space = []
car_counts = list(range(10, 50, 10))
for cuantos in car_counts:
    build_routes(cuantos, 60, types, duplicate=True)
    run_simulation()
    time_avg = time_average(start=30)
    # space_avg = space_average()
    time_avg = time_avg['car'].rename('car_' + str(cuantos))
    # space_avg = space_avg['car']['speed'].rename('car_' + str(cuantos))
    resultados_time.append(time_avg)
    # resultados_space.append(space_avg)

# Escribo sólo los últimos, para probar:
write_advisor_files()
car_time = DataFrame(resultados_time).transpose()
# car_space = DataFrame(resultados_space).transpose()

# fig, axes = plt.subplots(nrows=1, ncols=2)
car_time.plot()
# car_space.plot(ax=axes[1])
plt.show()

# Experimento para cortar todos los ciclos a partir de 50 metros
# y graficarlos
build_routes(30, 60, types, duplicate=True)
run_simulation()
datos = {}
parsed_vehicles = v_type_probe_parse('data/output/salida.xml')
for k, v in parsed_vehicles.items():
    if 'car' in k:
        df = v.as_DataFrame()
        start_index = min(df[df['position'] > 250].index.tolist())
        df = df[start_index:]
        df = df.reset_index(drop=True)
        datos[k] = df

out = pd.concat(datos.values(), axis=1, keys=datos.keys())
out_flat = out.stack(0).reset_index().drop('level_0', axis=1)
g = sns.FacetGrid(out_flat, hue='level_1', size=5)
g.map(plt.scatter, 'position', 'speed', s=10, alpha=0.6)
g.map(plt.plot, 'position', 'speed', linewidth=0.5, alpha=0.6)
plt.show()
