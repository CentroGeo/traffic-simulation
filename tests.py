# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
from pandas import DataFrame
from sumo_utilities.simulation import build_routes, run_simulation, parse_types
from sumo_utilities.driving_cycles import time_average

matplotlib.style.use('ggplot')
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'
TYPES = 'data/new_types.csv'

types = parse_types('data/new_types.csv')
resultados = []
car_counts = list(range(10, 200, 10))
for cuantos in car_counts:
    print(cuantos)
    build_routes(cuantos, 60, types, duplicate=True)
    run_simulation()
    avg_df = time_average(start=30)
    avg_car = avg_df['car'].rename('car_' + str(cuantos))
    resultados.append(avg_car)

car_df = DataFrame(resultados).transpose()
fig, ax = plt.subplots()
car_df.plot(ax=ax)
plt.show()
