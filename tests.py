# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
from pandas import DataFrame
from sumo_utilities.simulation import build_routes, run_simulation, parse_types
from sumo_utilities.driving_cycles import time_average, space_average

matplotlib.style.use('ggplot')
# Constants
NET = 'data/sumo_topes_2016.net.xml'
OUT_FLOWS = 'data/hourly_flows.xml'
OUT_ROUTS = 'data/routes.rou.xml'
CONFIG = 'data/adhoc.sumocfg'
TYPES = 'data/new_types.csv'

types = parse_types('data/new_types.csv')
resultados_time = []
resultados_space = []
car_counts = list(range(10, 100, 10))
for cuantos in car_counts:
    build_routes(cuantos, 60, types, duplicate=True)
    run_simulation()
    time_avg = time_average(start=30)
    space_avg = space_average()
    time_avg = time_avg['car'].rename('car_' + str(cuantos))
    space_avg = space_avg['car']['speed'].rename('car_' + str(cuantos))
    resultados_time.append(time_avg)
    resultados_space.append(space_avg)

car_time = DataFrame(resultados_time).transpose()
car_space = DataFrame(resultados_space).transpose()

fig, axes = plt.subplots(nrows=1, ncols=2)
car_time.plot(ax=axes[0])
car_space.plot(ax=axes[1])
plt.show()
